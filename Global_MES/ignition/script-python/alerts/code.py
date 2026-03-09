def showAlert(state, 
			title, 
			message, 
			btnTextPrimary,
			btnActionPrimary,
			btnTextSecondary = '',
			btnIconPrimary = '',
			btnIconSecondary = '', 
			btnIconAlignment = 'right',  
			btnActionSecondary = 'closePopup',
			showCloseBtn = True, 
			btnActionClose = 'closePopup'):
	
	
	
	params = {
		"state":state, 
		"title":title, 
		"message":message, 
		"showCloseBtn":showCloseBtn, 
		"btnTextPrimary":btnTextPrimary, 
		"btnTextSecondary":btnTextSecondary, 
		"btnIconPrimary":btnIconPrimary, 
		"btnIconSecondary":btnIconSecondary, 
		"btnIconAlignment":btnIconAlignment, 
		"btnActionPrimary":btnActionPrimary, 
		"btnActionSecondary":btnActionSecondary, 
		"btnActionClose":btnActionClose
	}
	
	system.perspective.openPopup(id="alertDialog", 
								view="Alerts/alert", 
								params=params, 
								showCloseIcon=False, 
								draggable=False, 
								resizable=False,
								modal=True, 
								overlayDismiss=True
								)
	

def noSelectionTable(function):
	alerts.showAlert(state='info', 
						title='Seleccione fila', 
						message='Seleccione ' + function,
						btnTextPrimary='Aceptar',
						btnActionPrimary=''
					)



def noSelectionOption(function):
	alerts.showAlert(state='info', 
						title='Seleccione Opcion', 
						message='Seleccione ' + function,
						btnTextPrimary='Aceptar',
						btnActionPrimary=''
					)

def noValidOption(function):
	alerts.showAlert(state='info', 
						title='Seleccion no valida', 
						message=function,
						btnTextPrimary='Aceptar',
						btnActionPrimary=''
					)

def confirmDelete(title, message, deleteAction):
	alerts.showAlert(state='warning', 
						title=title, 
						message='Seguro que desea eliminar ' + message,
						btnTextPrimary='Eliminar',
						btnActionPrimary=deleteAction,
						btnTextSecondary='Cancelar'
					)

def confirmAction(title, message, action):
	alerts.showAlert(state='info', 
						title=title, 
						message='Seguro que desea ' + message,
						btnTextPrimary='Aceptar',
						btnActionPrimary=action,
						btnTextSecondary='Cancelar'
					)
					
def actionSuccess(title, message):
	alerts.showAlert(state = 'success', 
					title = title, 
					message = message,
					btnTextPrimary='Aceptar',
					btnActionPrimary=''
					)
					

def actionDeleteError(title, message):
    alerts.showAlert(state='error', 
              title=title, 
              message=message, 
              btnTextPrimary='Aceptar',
              btnActionPrimary=''
              )

def showAlertAndComment(state,
						title,
						message,
						showCloseBtn,
						btnTextPrimary,
						btnTextSecondary,
						btnIconPrimary,
						btnIconSecondary,
						btnIconAlignment,
						btnActionPrimary,
						btnActionSecondary,
						btnActionClose):
							
	params = {"state":state,
			"title":title,
			"message":message,
			"showCloseBtn":showCloseBtn,
			"btnTextPrimary":btnTextPrimary,
			"btnTextSecondary":btnTextSecondary,
			"btnIconPrimary":btnIconPrimary,
			"btnIconSecondary":btnIconSecondary,
			"btnIconAlignment":btnIconAlignment,
			"btnActionPrimary":btnActionPrimary,
			"btnActionSecondary":btnActionSecondary,
			"btnActionClose":btnActionClose}
			
	system.perspective.openPopup(id="alertDialog",
								view="Alerts/alertAndComment",
								params=params,
								showCloseIcon=False,
								draggable=False,
								resizable=False,
								modal=True,
								overlayDismiss=True,
								btnActionPrimary="closePopup")
								
def showAlertAndDropdown(state,
						title,
						message,
						showCloseBtn,
						btnTextPrimary,
						btnTextSecondary,
						btnIconPrimary,
						btnIconSecondary,
						btnIconAlignment,
						btnActionPrimary,
						btnActionSecondary,
						btnActionClose,
						dropdownoptions):
							
	params = {"state":state,
			"title":title,
			"message":message,
			"showCloseBtn":showCloseBtn,
			"btnTextPrimary":btnTextPrimary,
			"btnTextSecondary":btnTextSecondary,
			"btnIconPrimary":btnIconPrimary,
			"btnIconSecondary":btnIconSecondary,
			"btnIconAlignment":btnIconAlignment,
			"btnActionPrimary":btnActionPrimary,
			"btnActionSecondary":btnActionSecondary,
			"btnActionClose":btnActionClose,
			"options":dropdownoptions}
			
	system.perspective.openPopup(id="alertDialog",
								view="Alerts/alertAndDropdown",
								params=params,
								showCloseIcon=False,
								draggable=False,
								resizable=False,
								modal=True,
								overlayDismiss=True,
								btnActionPrimary="closePopup")
	