import os
import sys
import shutil
import argparse
from pathlib import Path
from PIL import Image
import cv2
import numpy as np
import torch
from transformers import ViTImageProcessor, ViTForImageClassification
from transformers import pipeline

class ContentFilter:
    def __init__(self):
        # Initialize directories
        self.bad_dir = "bad"
        self.good_dir = "good"
        self.fail_dir = "fail"
        
        # Supported file extensions
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
        self.video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.ts', '.wmv', '.flv', '.webm'}
        
        # Initialize models
        self.init_models()
        
    def init_models(self):
        """Initialize AI models for content detection"""
        try:
            print("Loading AI models...")
            
            # Load NSFW detection model
            self.nsfw_classifier = pipeline(
                "image-classification",
                model="Falconsai/nsfw_image_detection",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Load blood/feces detection model (using general content classification)
            self.content_classifier = pipeline(
                "image-classification",
                model="google/vit-base-patch16-224",
                device=0 if torch.cuda.is_available() else -1
            )
            
            print("Models loaded successfully!")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            print("Please ensure you have internet connection for model download")
            sys.exit(1)
    
    def create_directories(self, base_path):
        """Create output directories if they don't exist"""
        for dir_name in [self.bad_dir, self.good_dir, self.fail_dir]:
            dir_path = os.path.join(base_path, dir_name)
            os.makedirs(dir_path, exist_ok=True)
    
    def extract_frames_from_video(self, video_path, max_frames=5):
        """Extract key frames from video for analysis"""
        frames = []
        try:
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Extract frames at regular intervals
            frame_indices = np.linspace(0, total_frames-1, max_frames, dtype=int)
            
            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(Image.fromarray(frame_rgb))
            
            cap.release()
            return frames
            
        except Exception as e:
            print(f"Error processing video {video_path}: {e}")
            return []
    
    def analyze_image(self, image):
        """Analyze image for inappropriate content"""
        try:
            # NSFW detection
            nsfw_results = self.nsfw_classifier(image)
            nsfw_score = next((result['score'] for result in nsfw_results 
                             if result['label'].lower() in ['nsfw', 'explicit']), 0)
            
            # General content analysis for blood/feces
            content_results = self.content_classifier(image)
            
            # Check for potentially inappropriate content
            inappropriate_labels = ['blood', 'wound', 'injury', 'medical', 'gross', 'dirty']
            content_score = max([result['score'] for result in content_results 
                               if any(label in result['label'].lower() for label in inappropriate_labels)], default=0)
            
            # Determine if content is inappropriate
            if nsfw_score > 0.7 or content_score > 0.6:
                return 'bad', f"NSFW: {nsfw_score:.2f}, Content: {content_score:.2f}"
            elif nsfw_score < 0.3 and content_score < 0.3:
                return 'good', f"NSFW: {nsfw_score:.2f}, Content: {content_score:.2f}"
            else:
                return 'fail', f"Uncertain - NSFW: {nsfw_score:.2f}, Content: {content_score:.2f}"
                
        except Exception as e:
            return 'fail', f"Error: {str(e)}"
    
    def process_file(self, file_path, base_path):
        """Process a single file"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in self.image_extensions:
                # Process image
                image = Image.open(file_path)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                result, reason = self.analyze_image(image)
                
            elif file_ext in self.video_extensions:
                # Process video (extract frames and analyze)
                frames = self.extract_frames_from_video(file_path)
                if not frames:
                    return 'fail', "Could not extract frames from video"
                
                # Analyze each frame and take the worst result
                results = []
                for frame in frames:
                    frame_result, frame_reason = self.analyze_image(frame)
                    results.append((frame_result, frame_reason))
                
                # If any frame is bad, mark the whole video as bad
                if any(result[0] == 'bad' for result in results):
                    result = 'bad'
                    reason = "Contains inappropriate frames"
                elif all(result[0] == 'good' for result in results):
                    result = 'good'
                    reason = "All frames appropriate"
                else:
                    result = 'fail'
                    reason = "Mixed or uncertain content"
            else:
                return 'fail', "Unsupported file type"
            
            # Move file to appropriate directory
            dest_dir = os.path.join(base_path, result)
            dest_path = os.path.join(dest_dir, os.path.basename(file_path))
            
            # Handle filename conflicts
            counter = 1
            while os.path.exists(dest_path):
                name, ext = os.path.splitext(os.path.basename(file_path))
                dest_path = os.path.join(dest_dir, f"{name}_{counter}{ext}")
                counter += 1
            
            shutil.move(file_path, dest_path)
            
            return result, reason
            
        except Exception as e:
            # Move to fail directory on error
            fail_path = os.path.join(base_path, self.fail_dir, os.path.basename(file_path))
            try:
                shutil.move(file_path, fail_path)
            except:
                pass
            return 'fail', f"Processing error: {str(e)}"
    
    def scan_directory(self, directory_path):
        """Scan directory and process all supported files"""
        print(f"Scanning directory: {directory_path}")
        
        # Create output directories
        self.create_directories(directory_path)
        
        # Get all files in directory
        files_to_process = []
        for root, dirs, files in os.walk(directory_path):
            # Skip output directories
            dirs[:] = [d for d in dirs if d not in [self.bad_dir, self.good_dir, self.fail_dir]]
            
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in self.image_extensions or file_ext in self.video_extensions:
                    files_to_process.append(os.path.join(root, file))
        
        if not files_to_process:
            print("No supported files found in the directory.")
            return
        
        print(f"Found {len(files_to_process)} files to process")
        
        # Process files
        good_count = 0
        bad_count = 0
        fail_count = 0
        
        for i, file_path in enumerate(files_to_process, 1):
            print(f"Processing {i}/{len(files_to_process)}: {os.path.basename(file_path)}")
            
            result, reason = self.process_file(file_path, directory_path)
            
            if result == 'good':
                good_count += 1
            elif result == 'bad':
                bad_count += 1
            else:
                fail_count += 1
            
            print(f"  -> {result.upper()}: {reason}")
        
        # Print summary
        print("\n" + "="*50)
        print("PROCESSING SUMMARY")
        print("="*50)
        print(f"Total files processed: {len(files_to_process)}")
        print(f"Good files: {good_count}")
        print(f"Bad files: {bad_count}")
        print(f"Failed files: {fail_count}")
        print("="*50)

def main():
    parser = argparse.ArgumentParser(description='Content Filter for Images and Videos')
    parser.add_argument('path', nargs='?', default='.', 
                       help='Directory path to scan (default: current directory)')
    
    args = parser.parse_args()
    
    # Convert to absolute path
    scan_path = os.path.abspath(args.path)
    
    if not os.path.isdir(scan_path):
        print(f"Error: Directory '{scan_path}' does not exist.")
        sys.exit(1)
    
    # Initialize and run filter
    filter_system = ContentFilter()
    filter_system.scan_directory(scan_path)

if __name__ == "__main__":
    main()
