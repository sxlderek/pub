### PURPOSE: set windows languages
### USAGE  : scriptname [Arguments]
### LICENSE: MIT License / (C) @sxlderek
### #
### Argument    Purpose

#Requires -PSEdition Desktop  # not Core edition
#Requires -Version 5.1        # Win 10
#Requires -RunAsAdministrator

param ( [string] $Action="help" )

function showhelp {
    Select-String -Path $PSCommandPath -Pattern ("##\#(.*)") `
        | ForEach-Object {$_.Matches.Groups[1].Value}
}

#set hk imput methods
function set_hkime {
    $LanguageList = New-WinUserLanguageList -Language zh-HK
    $LanguageList[0].Handwriting = $True
    $LanguageList[0].InputMethodTips.Clear()
    $ime="0404:{531FDEBF-9B4C-4A43-A2AA-960E8FCDC732}"
    $ime+="{6024B45F-5C54-11D4-B921-0080C882687E}" #速成
    $LanguageList[0].InputMethodTips.Add("$ime}")
    $ime="0404:{531FDEBF-9B4C-4A43-A2AA-960E8FCDC732}"
    $ime+="{4BDF9F03-C7D3-11D4-B2AB-0080C882687E}" #倉頡
    $LanguageList[0].InputMethodTips.Add("$ime}")
    Set-WinUserLanguageList -Force -LanguageList $LanguageList
}

#set china imput methods
function set_cnime {
    $LanguageList = New-WinUserLanguageList -Language zh-CN
    $LanguageList[0].Handwriting = $True
    $LanguageList[0].InputMethodTips.Clear()
    $ime="0804:{81D4E9C9-1D3B-41BC-9E6C-4B40BF79E35E}"
    $ime+="{FA550B04-5AD7-411F-A5AC-CA038EC515D7}" #併音
    $LanguageList[0].InputMethodTips.Add("$ime") 
    $ime="0804:{6A498709-E00B-4C45-A018-8F9E4081AE40}"
    $ime+="{82590C13-F4DD-44F4-BA1D-8667246FDF8E}" #五筆
    $LanguageList[0].InputMethodTips.Add("$ime") 
    Set-WinUserLanguageList -Force -LanguageList $LanguageList    
}

Write-Host "$Action"
#Set-PSDebug -Trace 2

# ref: https://is.gd/PxWSbH
Switch ($Action) {
    help {
        ### help        display help
        showhelp
    }

    hken {
        ### hken        HK ENG only user
        Install-Language -Language en-US -CopyToSettings # -AsJob 
        Set-TimeZone -Id "China Standard Time"
        Set-Culture -CultureInfo en-HK
        Set-Culture en-HK
        Set-WinSystemLocale -SystemLocale en-HK
        Set-WinHomeLocation -GeoId 104  # set location to hk
        Set-WinLanguageBarOption  # reset the language bar
        $UserLanguageList = New-WinUserLanguageList -Language en-US
        Set-WinUserLanguageList -Force -LanguageList $UserLanguageList
        Set-WinUILanguageOverride -Language en-HK
    }

    hkct {
        ### hkct        HK CHT 速成(quick) 倉頡(cangjie)
        Install-Language -Language en-US # -AsJob
        Install-Language -Language zh-HK -CopyToSettings # -AsJob
        Set-TimeZone -Id "China Standard Time"
        Set-Culture -CultureInfo zh-HK
        Set-WinSystemLocale -SystemLocale zh-HK
        Set-WinHomeLocation -GeoId 104  # set location to hk
        Set-WinLanguageBarOption  # reset the language bar
        set_hkime
        Set-WinUILanguageOverride -Language zh-HK
    }

    hkenct {
        ### hkenct      HK EN display, CHT input 速成(quick) 倉頡(cangjie)
        Install-Language -Language en-US -CopyToSettings # -AsJob
        Install-Language -Language zh-HK # -AsJob
        Set-TimeZone -Id "China Standard Time"
        Set-Culture -CultureInfo en-HK
        Set-WinSystemLocale -SystemLocale en-HK
        Set-WinHomeLocation -GeoId 104  # set location to hk
        Set-WinLanguageBarOption  # reset the language bar
        set_hkime
        Set-WinUILanguageOverride -Language en-HK       
    }

    cn {
        ### cn          CN 併音(pinyin) 五筆(wubi)
        Install-Language -Language en-US # -AsJob
        Install-Language -Language zh-CN -CopyToSettings # -AsJob
        Set-TimeZone -Id "China Standard Time"
        Set-Culture -CultureInfo zh-CN
        Set-WinSystemLocale -SystemLocale zh-CN
        Set-WinHomeLocation -GeoId 45  # set location to cn
        Set-WinLanguageBarOption  # reset the language bar
        set_cnime
        Set-WinUILanguageOverride -Language zh-CN       
    }

    jp {
        ### jp          JP 日本語
        Install-Language -Language en-US # -AsJob
        Install-Language -Language ja-JP -CopyToSettings  # -AsJob 
        Set-TimeZone -Id "Tokyo Standard Time"
        Set-Culture -CultureInfo ja-JP
        Set-WinSystemLocale -SystemLocale ja-JP
        Set-WinHomeLocation -GeoId 122  # set location to jp
        Set-WinLanguageBarOption  # reset the language bar
        $LanguageList = New-WinUserLanguageList -Language en-US
        $LanguageList.Add("ja-JP")
        $LanguageList[1].Handwriting = $True
        $LanguageList[1].InputMethodTips.Clear()
        $ime="0411:{03B5835F-F03C-411B-9CE2-AA23E1171E36}"
        $ime+="{A76C93D9-5523-4E90-AAFA-4DB112F9AC76}" #日本語
        $LanguageList[1].InputMethodTips.Add("$ime") #ja-JP
        Set-WinUserLanguageList -Force -LanguageList $LanguageList
        Set-WinUILanguageOverride -Language ja-JP
    }

    us {
        ### us          US ENG only user
        Install-Language -Language en-US -CopyToSettings # -AsJob 
        Set-TimeZone -Id "China Standard Time"
        Set-Culture -CultureInfo en-US
        Set-WinUILanguageOverride -Language en-US
        Set-WinSystemLocale -SystemLocale en-US
        Set-WinHomeLocation -GeoId 0xF4 # set location to US
        Set-WinLanguageBarOption  # reset the language bar
        $UserLanguageList = New-WinUserLanguageList -Language en-US
        Set-WinUserLanguageList -Force -LanguageList $UserLanguageList
        Set-WinDefaultInputMethodOverride -InputTip "0409:00000409"
        Write-host "Manually change timezone if not in HK"
    }
}

Set-PSDebug -Off
if ( $OSVersion.Major -gt 10 ) { Copy-UserInternationalSettingsToSystem 
    -WelcomeScreen $True -NewUser $True }
Write-host "Restart-Computer"
