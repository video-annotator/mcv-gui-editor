from mcvgui.core.editor.viewers.base_viewer import BaseViewer
from PyQt4 import QtCore, QtGui
from pyforms.controls import ControlTree

class ViewerModulesListWidget(ControlTree, BaseViewer):
	"""
	Class that implements the list graphical perspectives of the current project
	"""

	def __init__ (self, parentController = None):
		BaseViewer.__init__(self, parentController)
		ControlTree.__init__(self, 'Plugins view')

		self.showHeader   = False
		self.iconsize     = 64, 64

		self.addPopupMenuOption('Rename', self.__renameModule)
		self.addPopupMenuOption('Delete', self.projectsTreeItemDelete)
		
	############################################################################
	############ Interface events ##############################################
	############################################################################

	def __renameModule(self):
		if self._project!=None and self.mouseSelectedRowIndex!=None:
			item = self.topLevelItem(self.mouseSelectedRowIndex)
			text, ok = QtGui.QInputDialog.getText(self, 'Item name',  'Enter the new name:', text=item.text(0) )
			if ok:
				name = str(text)
				haveSameName = self._project.findModulesWithName(name)
				if len(haveSameName)>0: name += ' '+str(len(haveSameName)) 
				item.setText(0, name)
				item.module.name = name


	def projectsTreeItemDelete(self):
		if self._project!=None and self.mouseSelectedRowIndex!=None:
			item = self.topLevelItem(self.mouseSelectedRowIndex)
			self._project -= item.module
			self -= self.mouseSelectedRowIndex

	def treeItemSelected(self, index):
		"""
		Viewer item selected event
		@param index: Viewer item selected
		@type index: QModelIndex
		"""
		module = self._project.modulesOrdered[ index.row() ]
		module.show()
		self._selected = module

	############################################################################
	############ Parent class functions reemplementation #######################
	############################################################################
		
	def updateView(self, project):
		"""
		BaseViewer.updateView reimplementation
		@param project: Project object
		@type project: OTModuleProject
		"""
		BaseViewer.updateView(self, project)

		self.clear()
		if project!=None: 
			for module in project.modulesOrdered:
				treeItem = QtGui.QTreeWidgetItem([module.name])

				treeItem.setIcon( 0, QtGui.QIcon(module._iconFile) )
				treeItem.module = module
				self += treeItem