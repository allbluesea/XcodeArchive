#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os, time, subprocess
from optparse import OptionParser

import requests

from console_style import attrtext

CONFIGURATION = 'Debug'

# configuration for pgyer
PGYER_UPLOAD_URL = 'https://www.pgyer.com/apiv2/app/upload'
DOWNLOAD_BASE_URL = 'https://www.pgyer.com'
USER_KEY = 'df00dc35666d7196c62e029085443fe4'
API_KEY = 'd6e74aee5656dd9fc8590a401908b247'

def cleanBuildDir(buildDir):
	cleanCmd = 'rm -r %s' % (buildDir)
	process = subprocess.Popen(cleanCmd, shell=True)
	process.wait()
	print('clean build dir: %s' % buildDir)

def parseUploadResult(jsonResult):
	resultCode = jsonResult['code']
	if resultCode == 0:
		url = DOWNLOAD_BASE_URL + '/' + jsonResult['data']['buildShortcutUrl']
		print('%s\nDownload Url : %s\n' % (attrtext('\n** UPLOAD SUCCEEDED **\n', mode='bold'), url))
	else:
		print('Upload Failed!\nReason: ', jsonResult['message'])

def uploadIpaToPgyer(ipaPath):
# 	_api_key	String	(必填) API Key 点击获取_api_key
# 	file	File	(必填) 需要上传的ipa或者apk文件
# 	buildInstallType	Integer	(选填)应用安装方式，值为(1,2,3)。1：公开，2：密码安装，3：邀请安装。默认为1公开
# 	buildPassword	String	(选填) 设置App安装密码，如果不想设置密码，请传空字符串，或不传。
# 	buildUpdateDescription	String	(选填) 版本更新描述，请传空字符串，或不传。
# 	buildName	String	(选填) 应用名称

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

def buildProject(project, scheme, output=None, manual=False):
	process = subprocess.Popen('pwd', stdout=subprocess.PIPE)
	(stdoutdata, stderrdata) = process.communicate()
	stdout = str(stdoutdata, encoding='utf-8')

	timestamp = int(time.time())
	archiveDir = '~/Desktop/XcodeAPP/Archive/%s_%d.xcarchive' % (scheme, timestamp)
	archiveCmd = 'xcodebuild archive -project %s -scheme %s -configuration %s -archivePath %s' %(project, scheme, CONFIGURATION, archiveDir)
	process = subprocess.Popen(archiveCmd, shell=True)
	process.wait()

	if output is None:
		output = '~/Desktop/IPA/%s_%d' % (scheme, timestamp) 
	plistPath = stdout.strip() + '/options.plist'
	exportArchiveCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s' % (archiveDir, output, plistPath)
	process = subprocess.Popen(exportArchiveCmd, shell=True)
	(stdoutdata, stderrdata) = process.communicate()

	if not manual:
		ipaPath = output + '/%s.ipa' % scheme
		abspath = os.path.expanduser(ipaPath)
		if os.path.iffile(abspath):
			uploadIpaToPgyer(abspath)
		else:
			print('err: ipa dose not exists')
		#cleanBuildDir('./build')

def buildWorkspace(workspace, scheme, output=None, manual=False):
	process = subprocess.Popen('pwd', stdout=subprocess.PIPE)
	(stdoutdata, stderrdata) = process.communicate()
	stdout = str(stdoutdata, encoding='utf-8')

	timestamp = int(time.time())
	archiveDir = '~/Desktop/XcodeAPP/Archive/%s_%d.xcarchive' % (scheme, timestamp)
	archiveCmd = 'xcodebuild archive -workspace %s -scheme %s -configuration %s -archivePath %s' % (workspace, scheme, CONFIGURATION, archiveDir)
	process = subprocess.Popen(archiveCmd, shell=True)
	process.wait()

	if output is None:
		output = '~/Desktop/XcodeAPP/IPA/%s_%d' % (scheme, timestamp)

	plistPath = stdout.strip() + '/options.plist'
	exportArchiveCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s' % (archiveDir, output, plistPath)
	process = subprocess.Popen(exportArchiveCmd, shell=True)
	(stdoutdata, stderrdata) = process.communicate()
	
	if not manual:
		ipaPath = output + '/%s.ipa' % scheme
		abspath = os.path.expanduser(ipaPath)
		if os.path.iffile(abspath):
			uploadIpaToPgyer(abspath)
		else:
			print('err: ipa dose not exists')
	# cleanBuildDir(buildDir)

def xcbuild(options):
	project = options.project
	workspace = options.workspace
	scheme = options.name
	output = options.output
	manual = options.manual

	if project is None and workspace is None:
		print('Warning: you must provide the parms project or workspace...')
	elif project is not None:
		buildProject(project, scheme, output, manual)
	elif workspace is not None:
		buildWorkspace(workspace, scheme, output, manual)

def main():
	parser = OptionParser()
	parser.add_option('-w', '--workspace', help='Build the workspace name.xcworkspace.', metavar='name.xcworkspace')
	parser.add_option('-p', '--project', help='Build the project name.xcodeproj.', metavar='name.xcodeproj')
	parser.add_option('-n', '--name', help='The scheme/target name specified if bulid a workspace/project， required if is workspace.', metavar='scheme/target')
	parser.add_option('-o', '--output', help='Specify output filePath', metavar='output_filePath')
	parser.add_option('-m', '--manual', action='store_true', help='Upload to the pyger platform manualy or automatically , default by automatically')

	(options, args) = parser.parse_args()
	
	xcbuild(options)

if __name__ == '__main__':
	# main()
	cleanBuildDir('123')
