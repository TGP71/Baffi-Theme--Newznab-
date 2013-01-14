#!/usr/bin/env python

# Written by convict

import sys, os, shutil

def install(update=False):
	# copy theme folders
	folders = ['baffi', 'baffi-green', 'baffi-red']
	for fname in folders:
		destination = os.path.join('../www/views/themes/', fname)
		try:
			shutil.copytree(fname, destination)
		except OSError, e:
			print 'Error copying theme folders: %s' % e

	# if this is not an update then backup pre-existing files
	if update == False:
		raw_input('Go and select the baffi theme in admin->site edit. Press enter to continue...')
		try:
			shutil.copy('../www/views/scripts/utils.js', '../www/views/scripts/utils_old_original.js')
			os.rename('../www/views/scripts/utils.js', '../www/views/scripts/utils_old.js')
			shutil.copy('../www/lib/framework/basepage.php', '../www/lib/framework/basepage_old_original.php')
			os.rename('../www/lib/framework/basepage.php', '../www/lib/framework/basepage_old.php')
		except OSError, e:
			print 'Error copying/renaming frameworks: %s' % e

	# copy files to www/views/scripts
	files = ['bootstrap.js', 'utils.js', 'jquery.pnotify.js']
	for fname in files:
		destination = os.path.join('../www/views/scripts/', fname)
		try:
			shutil.copy(fname, destination)
		except OSError, e:
			print 'Error copying scripts: %s' % e

	# copy over baffi template folder and basepage.php
	try:
		shutil.copytree('templates_baffi', '../www/views/templates_baffi')
		shutil.copy('basepage.php', '../www/lib/framework/')
	except OSError, e:
			print 'Error copying template/basepage: %s' % e

def uninstall(update=False):
	# remove old theme folders
	try:
		folders = ['baffi', 'baffi-green', 'baffi-red']
		for fname in folders:
			shutil.rmtree(os.path.join('../www/views/themes/', fname))
	except OSError, e:
		print 'Error removing themes: %s' % e
	# remove old scripts
	try:
		files = ['bootstrap.js', 'utils.js', 'jquery.pnotify.js']
		for fname in files:
			os.remove(os.path.join('../www/views/scripts/', fname))
	except OSError, e:
		print 'Error removing old scripts: %s' % e
	# remove baffi:templates and basepage
	try:
		shutil.rmtree('../www/views/templates_baffi')
		os.remove('../www/lib/framework/basepage.php')
	except OSError, e:
		print 'Error removing templates/basepage: %s' % e

	# If this is an update, we don't want to revert old files
	if update == False:
		try:
			#revert to basepage backup
			os.rename('../www/lib/framework/basepage_old.php', '../www/lib/framework/basepage.php')
			#revert utils.js
			os.rename('../www/views/scripts/utils_old.js', '../www/views/scripts/utils.js')
		except OSError, e:
			print 'Unable to rever to old files: %s' % e

def preflight():
	if os.name != 'posix':
		sys.exit('This script is designed for linux. If you run this on windows and ask why it does not work I will come into your home and make a mess of your pots and pans.')
	if  os.geteuid() != 0:
		print "If you're having troubles or errors with this script please run it as root to see if the problem persists."
	dirs = ['../www/views/', '../www/views/scripts', '../www/views/themes', '../www/lib/', '../www/lib/framework', '../www/lib/smarty/templates_c']
	for folder in dirs:
		if os.path.isdir(folder) != True:
			sys.exit('ERROR: %s is not a directory. Are you calling this script from the right folder?' % folder)

def delcache():
	cache_dir = '../www/lib/smarty/templates_c'
	for root, dirs, files in os.walk(cache_dir):
		for name in files:
				try:
					os.remove(os.path.join(root, name))
				except OSError, e:
					print 'Warning: Could not clear smarty cache: %s' % e

def main(switch):
	preflight()
	if switch == 'install':
		install()
		print 'Finished!'
	if switch == 'uninstall':
		uninstall()
		print 'Finished!'
	if switch == 'update':
		uninstall(True)
		install(True)
		print 'Finished!'
	if switch == 'delcache':
		delcache()
		print 'Finished!'

if __name__ == '__main__':
	args = ['install', 'uninstall', 'update', 'delcache']
	usage = '''./runme.py [install, uninstall, update, delcache]
	!This folder must be located in the root of the newznab folder to run properly!'''

	if len(sys.argv) < 2:
		sys.exit(usage)
	if sys.argv[1] in args:
		main(sys.argv[1])
	else:
		sys.exit(usage)