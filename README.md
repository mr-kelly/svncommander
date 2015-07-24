# SvnCommander

一个对svn命令的封装器，解析并获取指定信息

比如获取指定目录的库URL

`

>>> import SvnCommander
>>> clientSvn = SvnCommander('path/svnpath', '../svn.exe')
>>> clientRepoUrl = clientSvn.getRepoUrl()
>>> print(clientRepoUrl)
http://svnpath/trunk

`


获取指定目录的Revision版本

`
>>> import SvnCommander
>>> clientSvn = SvnCommander('path/svnpath', '../svn.exe')
>>> revision = clientSvn.getHeadVersionNum()
>>> print(revision)

123

`



未经过严谨测试