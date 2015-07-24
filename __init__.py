#coding=utf-8
"""
SVN工具集, python指令调用svn系统命令

主要其实就是字符串处理

可跨平台使用哦

by Kelly (23110388@qq.com)
"""
import os
import subprocess
import tempfile
import argparse

# SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
# os.chdir(SCRIPTPATH)

svnDirPath = "https://cosmosbox/svn/cosmosbox/trunk/cb-product/AssetBundles/"
cmdSvnDiffVersion = """svn diff -r %s:%s """ + svnDirPath
cmdGetHeadVersionNum = "svn info -r HEAD "
cmdCheckout = "svn co %s -r %s %s" # url / version / targetPath
cmdSvnList = "svn list -v -R"
cmdChangeList = "svn status"

def shellCall(cmd):
	print "shellCall: '%s'" % cmd
	subprocess.call(cmd, shell=True);

def call(cmd):
	print "call: '%s'" % cmd
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

	return p.stdout.read()

class SvnCommander:
	def __init__(self, workPath, svnExePath):
		self.svnExePath = os.path.realpath(svnExePath)
		self.workPath = os.path.realpath(workPath)

	def getLines(self, strs):
		"""
		svn指令都是 xxx: vvvv格式, 输入xxx获取vvv, key不唯一时返回list

		>>> len(testCommander.getLines('abcdefg\\nasdaqwew\\n1235\\n'))
		3
		"""
		retList = [s.strip() for s in strs.split('\n') if s]
		return retList 

	def parseSvnResult(self, strs):
		"""

		>>> result = testCommander.parseSvnResult('abcd : ok!\\ndefg: not ok!')
		>>> result['abcd']
		'ok!'
		>>> result['defg']
		'not ok!'
		"""
		lines = self.getLines(strs)
		ret = {}
		for line in lines:
			lineArr = line.split(':', 1)
			if len(lineArr) >= 2:
				key = lineArr[0].strip()
				value = lineArr[1].strip()
				ret[key] = value

		return ret
	def getInfo(self, strs, key):
		result = self.parseSvnResult(strs)
		if (result[key]):
			return result[key]
		return None

	def merge(self, url):
		"""
		合并，传入url，与本地工作目录合并（不允许URL之间合并，太危险）
		"""
		shellCall('%s merge %s@HEAD %s' % (self.svnExePath, url, self.workPath))

	def update(self):
		shellCall('%s update' % (self.svnExePath))
		
	def switch(self, url):
		shellCall('%s switch %s %s' % (self.svnExePath, url, self.workPath))

	def getRepoUrl(self):
		"""
		>>> 'http' in testCommander.getRepoUrl()
		True
		"""
		_cmd = self.svnExePath + ' info -r HEAD ' + self.workPath
		result = call(_cmd)

		return self.getInfo(result, 'URL')

	def getDiffFiles(self, fromVersion, toVersion):
		"""
		获取版本变动的文件列表

		"""
		result = call(cmdSvnDiffVersion % (fromVersion, toVersion))

		return self.parseSvnResult(result)["Index"]

	def getHeadVersionNum(self):
		"""
		获取HEAD版本号

		>>> testCommander.getHeadVersionNum().isdigit()
		True
		"""
		result = call(cmdGetHeadVersionNum + self.workPath)
		return self.parseSvnResult(result)["Revision"]

	def GetTmpSvnDir(self, version):
		"""获取指定版本的临时文件夹"""
		tempPath = tempfile.gettempdir()
		versionDir = '_'.join(svnDirPath.split('/')[-3:])
		tempPath = os.path.join(tempPath, "CosmosSVN", "%s_%s" %(versionDir, version))

		return tempPath

	def CheckoutToTmpDir(self, version, tempPath):
		""" 临时文件夹，checkout指定版本 """
		print call(cmdCheckout % (svnDirPath, version, tempPath))

	def GetSvnList(self, strPath):
		""" 获取指定目录所有svn内文件及其信息"""
		os.chdir(strPath)
		return GetLines(call(cmdSvnList))


	def GetChangedList(self, strPath):
		""" 獲取指定目錄下面所有改動的文件 """
		os.chdir(strPath)
		lines = GetLines(call(cmdChangeList))
		retList = []
		for line in lines:
			if line[0] in ['?', 'M']:
				fRPath = line.replace('?', '').replace('M', '').strip()
				retList.append(fRPath)

		return 

	def GetDelList(self, strPath):
		"""
		獲取指定目錄下面所有刪除或missing的文件

		"""
		os.chdir(strPath)
		lines = GetLines(call(cmdChangeList))
		retList = []
		for line in lines:
			if line[0] in ['!', 'D']:
				fRPath = line.replace('!', '').replace('D', '').strip()
				retList.append(fRPath)

		return retList


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Svn Helper! TODO command line!")
	parser.add_argument("path")
	parser.add_argument("--svn_exe", default="svn.exe")
	parser.add_argument("--test", default=False)
	args = parser.parse_args()

	if args.test:
		import doctest
		doctest.testmod(extraglobs={'testCommander':SvnCommander(args.path, args.svn_exe)})
	else:
		print('do nothing! maybe you want to --test True ??')