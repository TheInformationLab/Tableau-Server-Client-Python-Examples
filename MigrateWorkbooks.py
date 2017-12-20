import tableauserverclient as TSC
# from tableaudocumentapi import Workbook
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Let's do some configuration....
# First, configure the source server
sourceServer = 'https://tableauserver'
sourceSiteID = 'site'
sourceUsername = 'username'
sourcePassword = 'password'
sourceAPIVersion = '2.7'
sourceWorkbook = 'Workbook Name'

# Now, configure the destination server
destinationServer = 'https://tableauserver'
destinationSiteID = 'site'
destinationUsername = 'user'
destinationPassword = 'password'
destinationAPIVersion = '2.7'
destinationProject = 'Default'
destinationWorkbook = 'Workbook Name'

# OK configuration is all done. You shouldn't need to modify anything else.
# If you want to modify a datasource along the way then take a look at the commented out section below

print("\nSigning into source server")
tableau_auth = TSC.TableauAuth(sourceUsername, sourcePassword, site_id=sourceSiteID)
server = TSC.Server(sourceServer)
server.version = sourceAPIVersion

with server.auth.sign_in(tableau_auth):
    print("\nLogged in to source server")
    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,TSC.RequestOptions.Operator.Equals,sourceWorkbook))
    all_workbooks, pagination_item = server.workbooks.get(req_option)
    downloaded_file = server.workbooks.download(all_workbooks[0].id, filepath=sourceWorkbook + '.twbx')
    print("\nDownloaded the file to {0}.".format(downloaded_file))

    # Need to modify any data connections along the way? Do them here
    #sourceWB = Workbook(downloaded_file)
    #sourceWB.datasources[0].connections[0].dbname = "newDB"
    #sourceWB.save_as(sourceWorkbook + '.twbx')
    #print("\nData connection updated and saved to {0}.twbx".format(sourceWorkbook))

print("\nLogged out of source server")
tableau_auth = TSC.TableauAuth(destinationUsername, destinationPassword, site_id=destinationSiteID)
server = TSC.Server(destinationServer)
server.version = destinationAPIVersion

print("\nSigning into destination server")
with server.auth.sign_in(tableau_auth):
    print("\nLogged in to destination server")
    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,TSC.RequestOptions.Operator.Equals,destinationProject))
    all_projects, pagination_item = server.projects.get(req_option)
    wb_item = TSC.WorkbookItem(name=destinationWorkbook, project_id=all_projects[0].id)
    print("\nPublishing workbook")
    wb_item = server.workbooks.publish(wb_item, sourceWorkbook + '.twbx', 'Overwrite')
    print("\nWorkbook published, all done!")
