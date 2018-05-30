
#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os, time, subprocess
from optparse import OptionParser

import requests

from console_style import attrtext


#configuration for iOS build setting

#CODE_SIGN_IDENTITY = "iPhone Distribution: xxxxxxxx Co. Ltd (xxxxxxx9A)"
#PROVISIONING_PROFILE = "xxxxxxxxxx-xxxxx-xxxxx-xxxx-xxxxxxxxxxxx"
#CONFIGURATION = "Release"
#SDK = "iphoneos"

CODE_SIGN_IDENTITY = ""
PROVISIONING_PROFILE = ""
CONFIGURATION = "Debug"
SDK = "iphoneos"

# configuration for pgyer
PGYER_UPLOAD_URL = "https://www.pgyer.com/apiv2/app/upload"
DOWNLOAD_BASE_URL = "http://www.pgyer.com"
USER_KEY = "xxxxxx" #replace with your pgyer userkey
API_KEY = "xxxxxx" #replace with your pgyer apikey

def cleanBuildDir(dir):
    if os.path.exists(dir):
        cleanCmd = 'rm -r %s' % (dir)
        process = subprocess.Popen(cleanCmd, shell=True)
        process.wait()
    


def parseUploadResult(jsonResult):
    resultCode = jsonResult['code']
    if resultCode == 0:
        url = DOWNLOAD_BASE_URL + '/' + jsonResult['data']['buildShortcutUrl']
        print('%s\nDownload Url : %s\n' % (attrtext('\n** UPLOAD SUCCEEDED **\n', mode='bold'), url))
    else:
        print('Upload Failed!\nReason: ', jsonResult['message'])

def uploadIpaToPgyer(ipaPath):
#   _api_key    String  (必填) API Key 点击获取_api_key
#   file    File    (必填) 需要上传的ipa或者apk文件
#   buildInstallType    Integer (选填)应用安装方式，值为(1,2,3)。1：公开，2：密码安装，3：邀请安装。默认为1公开
#   buildPassword   String  (选填) 设置App安装密码，如果不想设置密码，请传空字符串，或不传。
#   buildUpdateDescription  String  (选填) 版本更新描述，请传空字符串，或不传。
#   buildName   String  (选填) 应用名称

    files = {'file': open(ipaPath, 'rb')}
    headers = {'enctype':'multipart/form-data'}
    payload = {'_api_key':API_KEY, 'buildInstallType':'1'}
    print('From %s uploading to pgyer...' % ipaPath)
    r = requests.post(PGYER_UPLOAD_URL, data=payload, files=files, headers=headers)
    if r.status_code == requests.codes.ok:
         result = r.json()
         parseUploadResult(result)
    else:
        print('HTTP error occured, code: ', r.status_code)

def buildProject(project, target, output, manual=False):
    buildDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')

    if len(CODE_SIGN_IDENTITY) and len(PROVISIONING_PROFILE):
        buildCmd = 'xcodebuild -project %s -target %s -sdk %s -configuration %s build CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s" SYMROOT=%s' %(project, target, SDK, CONFIGURATION, CODE_SIGN_IDENTITY, PROVISIONING_PROFILE, buildDir)
    else:
        buildCmd = 'xcodebuild -project %s -target %s -sdk %s -configuration %s SYMROOT=%s' %(project, target, SDK, CONFIGURATION, buildDir)
    
    process = subprocess.Popen(buildCmd, shell = True)
    process.wait()
    
    if output is None:
        outputPath = os.path.expanduser('~/Desktop/XcodeAPP/IPA_ONLY')
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        timestamp = int(time.time())
        output = '%s/%s_%d.ipa' % (outputPath, target, timestamp)

    signApp = "%s/%s-iphoneos/%s.app" %(buildDir, CONFIGURATION, target)
    signCmd = "xcrun -sdk %s -v PackageApplication %s -o %s" %(SDK, signApp, output)
    process = subprocess.Popen(signCmd, shell=True)
    (stdoutdata, stderrdata) = process.communicate()
    
    if not manual:
        abspath = os.path.expanduser(output)
        if os.path.isfile(abspath):
            uploadIpaToPgyer(abspath)
        else:
            print(attrtext('Err: ipa does not exists', mode='bold', foreground_color='red'))

    cleanBuildDir(buildDir)

def buildWorkspace(workspace, scheme, output, manual=False):
    buildDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')

    if len(CODE_SIGN_IDENTITY) and len(PROVISIONING_PROFILE):
        buildCmd = 'xcodebuild -workspace %s -scheme %s -sdk %s -configuration %s build CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s" SYMROOT=%s' %(workspace, scheme, SDK, CONFIGURATION, CODE_SIGN_IDENTITY, PROVISIONING_PROFILE, buildDir)
    else:
        buildCmd = 'xcodebuild -workspace %s -scheme %s -sdk %s -configuration %s SYMROOT=%s' %(workspace, scheme, SDK, CONFIGURATION, buildDir)
    print(buildCmd)
    
    process = subprocess.Popen(buildCmd, shell=True)
    process.wait()
    
    if output is None:
        outputPath = os.path.expanduser('~/Desktop/XcodeAPP/IPA_ONLY')
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        timestamp = int(time.time())
        output = '%s/%s_%d.ipa' % (outputPath, scheme, timestamp)

    signApp = "%s/%s-iphoneos/%s.app" % (buildDir, CONFIGURATION, scheme)
    signCmd = "xcrun -sdk %s -v PackageApplication %s -o %s" % (SDK, signApp, output)
    process = subprocess.Popen(signCmd, shell=True)
    (stdoutdata, stderrdata) = process.communicate()
    
    if not manual:
        abspath = os.path.expanduser(output)
        if os.path.isfile(abspath):
            uploadIpaToPgyer(abspath)
        else:
            print(attrtext('Err: ipa does not exists', mode='bold', foreground_color='red'))

    cleanBuildDir(buildDir)

def xcbuild(options):
    project = options.project
    workspace = options.workspace
    name = options.name
    output = options.output
    manual = options.manual
    
    if project is None and workspace is None:
        print('Warning: you must provide the parms project or workspace...')
    elif project is not None:
        buildProject(project, name, output, manual)
    elif workspace is not None:
        buildWorkspace(workspace, name, output, manual)

def main():
    parser = OptionParser()
    parser.add_option("-w", "--workspace", help="Build the workspace name.xcworkspace.", metavar="name.xcworkspace")
    parser.add_option("-p", "--project", help="Build the project name.xcodeproj.", metavar="name.xcodeproj")
    parser.add_option("-n", "--name", help="The scheme/target name specified if bulid a workspace/project， required if is workspace.", metavar="scheme/target")
    parser.add_option("-o", "--output", help="specify output filePath+filename", metavar="output_filePath+filename")
    parser.add_option('-m', '--manual', action='store_true', help='Upload to the pyger platform manualy or automatically , default by automatically')
    
    (options, args) = parser.parse_args()
        
    xcbuild(options)

if __name__ == '__main__':
    main()
