angular.module('machadaloPages')
.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });

                event.preventDefault();
            }
        })
    }
})
.controller('userCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'userService','constants','$timeout','cfpLoadingBar','commonDataShare',
    function ($scope, $rootScope, $window, $location, userService, constants, $timeout, cfpLoadingBar, commonDataShare) {
        // reset login status
     $scope.model = {};
     $scope.cloneFromProfileId = {};
     console.log($rootScope);
     $scope.standardOrganisation = constants.standard_organisation;
     console.log($scope.standardOrganisation);
     $scope.permissionList = [];
     $scope.groupName = {};
     $scope.selectedGroupList = [];
     $scope.permissionsDict = [];
     $scope.userInfo = {};
     $scope.passwordError = constants.password_error;
     $scope.profileData = {};// to create profile
     $scope.organisationData = {}; // to create organisation
     $scope.organisationMappedIdList = []; // to create a list of organisation ids
     $scope.objectLevelPermissions = []; // list of object level permissions
     $scope.generalUserLevelPermissionData = {};// to create generalUserLevelPermissionData
     $scope.generalUserLevelPermissionsList = [];
     $scope.contentTypeObject = {};
     $scope.contentTypeListById = [];
     $scope.cloneProfileNewName = '';
     $scope.mappingData = {};


     $scope.userInfo = $rootScope.globals.userInfo;

     $scope.options = [
        {usercode : 'BD', id : '01'},
        {usercode : 'Ops', id: '02'},
        {usercode : 'Agency', id: '03'}
      ];

    $scope.userInfoHeaders = [
      {header : 'First Name'},
      {header : 'Last Name'},
      {header:  'Is SuperUser'},
      {header : 'Email Id'},
      {header : 'Username'},
      {header : 'Organisation'},
      {header : 'Profile'},
      {header : 'Edit'},
      {header : 'Delete'},
      {header : 'Change Password'},
    ];
    $scope.groupHeaders = [
      {header : 'Name of Group'},
      {header : 'Edit'},
      {header : 'Delete'},
    ]

    //to create organisation we should map that organisation to category
    $scope.organisationCategories = [
      'MACHADALO',
      'BUSINESS',
      'BUSINESS_AGENCY',
      'SUPPLIER_AGENCY',
      'SUPPLIER',
    ]
    $scope.operationOrganisation = {
      view : false,
      edit : false,
      create : false,
    }
    $scope.operationOnBoard = {
      organisation : true,
      profile : false,
      user : false,
    }

    $scope.operationProfile = angular.copy($scope.operationOrganisation);
      //To get permission list
      userService.getAllUserPermissions()
      .then(function onSuccess(response){
          console.log(response);
          $scope.permissions = response.data.data;
          addMoreFieldsToPermission();
          angular.forEach($scope.permissions, function(permission){
            $scope.permissionsDict[permission.id] = permission;
          })
          console.log($scope.permissionsDict);
        }).catch(function onError(response){
          commonDataShare.showErrorMessage(response);
            console.log("error occured");
        });

      var getAllUserGroups = function(){
      userService.getAllUserGroups()
      .then(function onSuccess(response){
        console.log(response);
        $scope.permissionGroups = response.data.data;
        addMoreFieldsToGroup();
        })
        .catch(function onError(response){
          commonDataShare.showErrorMessage(response);
            console.log("error occured");
        });
      }
      //get content types with model names
      var getContentTypes = function(){
        userService.getContentTypes()
        .then(function onSuccess(response){
          console.log(response);
          $scope.contentTypeList = response.data.data;
          angular.forEach($scope.contentTypeList, function(contentType){
            $scope.contentTypeListById[contentType.id] = contentType;
          })
        }).catch(function onError(response){
          console.log(response);
        })
      }
      $scope.getProfiles = function(organisationId){
        var promise = [];
        if(!organisationId)
          promise = userService.getProfiles()
        else
          promise = userService.getProfiles(organisationId)
        promise.then(function onSuccess(response){
          $scope.profilesList = response.data.data;
          console.log(response);
        }).catch(function onError(response){
          console.log(response);
        })
      }
      var getOrganisations = function(){
        userService.getOrganisations()
        .then(function onSuccess(response){
          $scope.organisationList = response.data.data;
          angular.forEach($scope.organisationList, function(organisation){
            $scope.organisationMappedIdList[organisation.organisation_id] = organisation;
          })
          console.log(response);
        }).catch(function onError(response){
          console.log(response);
        })
      }
      var getStandardProfileToClone = function(){
        userService.getStandardProfileToClone()
        .then(function onSuccess(response){
          $scope.standardProfileList = response.data.data;
          console.log(response);
        }).catch(function onError(response){
          console.log(response);
        })
      }
      //calling when page load
      getAllUserGroups();
      getContentTypes();
      $scope.getProfiles();
      getStandardProfileToClone();
      var addMoreFieldsToPermission = function(){
        angular.forEach($scope.permissions, function(permission){
          permission.selected = false;
        })
      }
      var addMoreFieldsToGroup = function(){
        angular.forEach($scope.permissionGroups, function(group){
          group.selected = false;
        });
      }
     $scope.register = function(wizardFinish){
      //  $scope.model['groups'] = $scope.selectedGroupList;
      console.log(wizardFinish);
      if ( !wizardFinish || ( wizardFinish && $scope.model.first_name && $scope.model.last_name && $scope.model.username && $scope.model.email && $scope.model.password) ) {
        if(wizardFinish)
          $scope.model['profile'] = $scope.clonedProfileId;
        userService.createUser($scope.model)
         .then(function onSuccess(response){
           console.log("Successful");
           $scope.selectedGroupList = [];
           $scope.model = {};
           addMoreFieldsToGroup();
           if(wizardFinish)
            $scope.getContent($scope.contentItem.organisationCommon);
           swal(constants.name,constants.createUser_success,constants.success);
           // alert("Successfully Created");
           })
           .catch(function onError(response){
               console.log("error occured");
               commonDataShare.showErrorMessage(response);
               // swal(constants.name,constants.errorMsg,constants.error);
               // alert("Error Occured");
           });
      }
     }
     //Start: to navigate menu list
     $scope.menuItem = [
       {name : 'createUser'},
       {name : 'createGroup'},
       {name : 'viewUsers'},
       {name : 'viewGroups'},
       {name : 'editUser'},
       {name : 'editGroup'},
       {name : 'profile'},
       {name : 'organisationCommon'},
       {name : 'organisation'},
       {name : 'profileView'},
       {name : 'onBoard'},
       {name : 'aboutYou'},
       {name : 'mapOrganisations'},
     ];
     $scope.contentItem = {
       createUser  : 'createUser',
       createGroup : 'createGroup',
       viewUsers   : 'viewUsers',
       viewGroups  : 'viewGroups',
       editUser    : 'editUser',
       editGroup    : 'editGroup',
       profile      : 'profile',
       organisation : 'organisation',
       organisationCommon : 'organisationCommon',
       profileView : 'profileView',
       onBoard    :   'onBoard',
       aboutYou   :   'aboutYou',
       mapOrganisations : 'mapOrganisations',
     }
     $scope.getContent = function(item,data){
       console.log(item);
       $scope.menuItem.name = item;
        switch(item){
          case $scope.contentItem.createUser:
            $scope.getProfiles();
            getOrganisations();
          case $scope.contentItem.viewUsers:
            getAllUsers();
            addMoreFieldsToGroup();
            getOrganisations();
            break;
          case $scope.contentItem.editUser:
            editUserInfo(data);
            addMoreFieldsToPermission();
            break;
          case $scope.contentItem.editGroup:
            $scope.permissionList = [];
            addMoreFieldsToGroup();
            $scope.menuItem.name = $scope.contentItem.createGroup;
            editGroupDetails(data);
            break;
          case $scope.contentItem.createGroup:
            $scope.isEditGroup = false;
            $scope.permissionList = [];
            addMoreFieldsToPermission();
            // $scope.permissions = [];
            $scope.groupName.name = null;
            break;
          case $scope.contentItem.organisationCommon:
            getOrganisations();
            break;
          case $scope.contentItem.profileView:
            $scope.getProfiles();
            // getObjectLevelPermissions();
            getOrganisations();
            // getGeneralUserLevelPermissions();
            break;
          case $scope.contentItem.onBoard:
            $scope.profileData = {};
            $scope.organisationData = {};
            $scope.cloneFromProfileId.id = null;
            $scope.activityNumber = 1;
            break;
          case $scope.contentItem.mapOrganisations:
            getOrganisationMappingList($scope.userInfo.profile.organisation.organisation_id);
            break;
        }
     }
     //End: to navigate menu list
     $scope.addPermission = function(permission,index){
       console.log($scope.userPermission);
       if(permission.selected == true)
        $scope.permissionList.push(permission)
       else{
         $timeout(function () {
           $scope.permissionList.splice($scope.permissionList.indexOf(permission),1);
        });
      }
     }
     $scope.createGroup = function(){
       console.log($scope.groupName);
       var permissions = [];
       angular.forEach($scope.permissionList,function(permission){
         console.log(permission);
        permissions.push(permission.id);
       });
       var data = {
         name : $scope.groupName.name,
         permissions : permissions,
       }
       console.log(data);
       userService.createGroup(data)
       .then(function onSuccess(response){
         console.log(response);
         $scope.groupName.name = null;
         $scope.permissionList = [];
         addMoreFieldsToPermission();
         getAllUserGroups();
         swal(constants.name,constants.create_group_success,constants.success);
       }).catch(function onError(response){
         console.log(response);
         commonDataShare.showErrorMessage(response);
        //  swal(constants.name,constants.create_group_error,constants.error);
       });
     }
    //start:adding groups
    $scope.addGroups = function(group,index){
      console.log(group);
      if(group.selected == true)
        $scope.selectedGroupList.push(group.name);
      else{
        $timeout(function () {
          $scope.selectedGroupList.splice($scope.selectedGroupList.indexOf(group.name),1);
       });
      }
      console.log($scope.selectedGroupList);
    }
    //end:adding groups
    $scope.validatePassword = function(){
      console.log("hello");
      if($scope.model.password == $scope.model.confirm_password)
        $scope.isValid = true;
      else
        $scope.isValid = false;
    }
    //start:get all users list
    var getAllUsers = function(){
      console.log("users calling");
      userService.getAllUsers()
      .then(function onSuccess(response){
        console.log(response);
        $scope.usersList = response.data.data;
      }).catch(function onError(response){
        commonDataShare.showErrorMessage(response);
        console.log(response);
      });
    }
    //end:get all users list
    // tooltip on edit and delete button
    $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip();
    });
    //start:edit user
    var editUserInfo = function(user){
      console.log(user);
      $scope.userDetails = user;
      angular.forEach($scope.userDetails.groups, function(group){
        for(var i=0;i<$scope.permissionGroups.length;i++){
          console.log(group);
          if(group.name == $scope.permissionGroups[i].name)
            $scope.permissionGroups[i].selected = true;
        }
      });
    }
    $scope.editUserGroups = function(group,index){
      if(group.selected == true)
        $scope.userDetails.groups.push(group);
      else{
        $timeout(function () {
          $scope.userDetails.groups.splice($scope.userDetails.groups.indexOf(group),1);
       });
      }
      // console.log($scope.selectedGroupList);
    }
    $scope.updateUserDetails = function(userDetails){
      var groups = [];
      angular.forEach(userDetails.groups, function(group){
        groups.push(group.id);
      });
      userDetails.groups = groups;
      userService.updateUserDetails(userDetails.id,userDetails)
      .then(function onSuccess(response){
        console.log(response);
        console.log(userDetails);
        swal(constants.name,constants.save_success,constants.success);
        $scope.getContent($scope.contentItem.viewUsers);
      }).catch(function onError(response){
        console.log(response);
        // commonDataShare.showErrorMessage(response);
        // swal(constants.name,constants.save_error,constants.error);
      });
    }
    //end:edit user
    //start: delete user
    $scope.deleteUser = function(user){
      swal({
         title: constants.warn_user_msg,
         text: constants.delete_confirm_user,
         type: constants.warning,
         showCancelButton: true,
         confirmButtonClass: constants.btn_success,
         confirmButtonText: constants.delete_confirm,
         closeOnConfirm: true
       },
       function(){
        console.log(user);
        userService.deleteUser(user.id)
        .then(function onSuccess(response){
          console.log(response);
          getAllUsers();
        }).catch(function onError(response){
          console.log(response);
          commonDataShare.showErrorMessage(response);
        });
      });
    }
    //end: delete user
    //start:code for edit group details
    var editGroupDetails = function (group){
      console.log(group);
      $scope.groupId = group.id;
      $scope.isEditGroup = true;
      $scope.groupName.name = group.name;
      console.log($scope.permissionsDict);
      angular.forEach(group.permissions, function(permission){
        console.log(permission);
        console.log($scope.permissionGroups);
        $scope.permissionsDict[permission].selected = true;
        $scope.permissionList.push($scope.permissionsDict[permission]);
        console.log($scope.permissionList);
      })
    }
    $scope.updateGroupDetails = function(){
      var permissions = [];
      angular.forEach($scope.permissionList,function(permission){
        console.log(permission);
       permissions.push(permission.id);
      });
      var data = {
        name : $scope.groupName.name,
        permissions : permissions,
      }
      userService.updateGroupDetails($scope.groupId,data)
      .then(function onSuccess(response){
        console.log(response);
        getAllUserGroups();
        swal(constants.name,constants.save_success,constants.success);
      }).catch(function onError(response){
        console.log(response);
        commonDataShare.showErrorMessage(response);
        // swal(constants.name,constants.save_error,constants.error);
      });
    }
    //end:code for edit group details
    //start : delete group code
    $scope.deleteGroup = function(group){
      console.log(group);
      swal({
         title: constants.warn_user_msg,
         text: constants.delete_confirm_group,
         type: constants.warning,
         showCancelButton: true,
         confirmButtonClass: constants.btn_success,
         confirmButtonText: constants.delete_confirm,
         closeOnConfirm: true
       },
       function(){
        userService.deleteGroup(group.id)
        .then(function onSuccess(response){
          console.log(response);
          getAllUserGroups();
        }).catch(function onError(response){
          console.log(response);
          commonDataShare.showErrorMessage(response);
        });
      });
    }

    //end : delete group code
    //start : change password
    $scope.setPasswordDetails = function(user){
      console.log(user);
      $scope.userInfo = user;
    }
    $scope.checkPassword = function(password,confirm_password){
      console.log(password,confirm_password);
      if(password == confirm_password)
          $scope.passwordValid = true;
      else
          $scope.passwordValid = false;
    }

    $scope.changePassword = function(){
      var data = {
        password : $scope.userInfo.password,
      }
      userService.changePassword($scope.userInfo.id,data)
      .then(function onSuccess(response){
        console.log(response);
        $scope.userInfo = {};
        commonDataShare.closeModal('#passwordModal');
        swal(constants.name,constants.changePassword_success,constants.success);
      }).catch(function onError(response){
        console.log(response);
        commonDataShare.showErrorMessage(response);
        // swal(constants.name,constants.errorMsg,constants.error);
      });
    }
    //end : change password

    //start: create organisation
    $scope.createOrganisation = function(){
      console.log($scope.organisationData);
      userService.createOrganisation($scope.organisationData)
      .then(function onSuccess(response){
        console.log(response);
        $scope.onBoardOrgId = response.data.data.organisation_id;
        swal(constants.name,constants.create_success,constants.success);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    //end: create organisation
    $scope.updateOrganisation = function(){
      userService.updateOrganisationDetails($scope.organisationData)
      .then(function onSuccess(response){
        console.log(response);
        swal(constants.name,constants.update_success,constants.success);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    $scope.goToOrganisation = function(contentItem, operation, data={}){
      console.log(data);
        $scope.organisationData = data;
        $scope.operationOrganisation.view = false;
        $scope.operationOrganisation.create = false;
        $scope.operationOrganisation.edit = false;
        $scope.operationOrganisation[operation] = true;
        $scope.getContent(contentItem);
    }

    //start: create profile
    $scope.createProfile = function(){
      userService.createProfile($scope.profileData)
      .then(function onSuccess(response){
        console.log(response);
        $scope.profileData = response.data.data;
        swal(constants.name,constants.create_success,constants.success);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    //end: create profile
    $scope.goToProfiles = function(contentItem, operation, data={}){
      $scope.profileData = data;
      $scope.operationProfile.view = false;
      $scope.operationProfile.create = false;
      $scope.operationProfile.edit = false;
      $scope.operationProfile[operation] = true;
      console.log($scope.profileData);
      $scope.profileData.organisation = $scope.profileData.organisation.organisation_id;
      $scope.getContent(contentItem);
    }
    $scope.updateProfile = function(){
      console.log($scope.profileData);
      userService.updateProfile($scope.profileData)
      .then(function onSuccess(response){
        console.log(response);
        swal(constants.name,constants.update_success,constants.success);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    //for generaluser permissionsDict
    var getObjectLevelPermissions = function(){
      userService.getObjectLevelPermissions()
      .then(function onSuccess(response){
        console.log(response);
        $scope.objectLevelPermissions = response.data.data;
      }).catch(function onError(response){
        console.log(response);
      })
    }
    $scope.createObjectLevelPermission = function(){
      console.log($scope.contentTypeObject);
      $scope.objectLevelPermissionData['name'] = $scope.contentTypeListById[$scope.objectLevelPermissionData.content_type].model.toUpperCase();
      console.log($scope.objectLevelPermissionData);
      userService.createObjectLevelPermission($scope.objectLevelPermissionData)
      .then(function onSuccess(response){
        console.log(response);
        if(!$scope.profileData.object_level_permission)
          $scope.profileData['object_level_permission'] = [];
        $scope.profileData['object_level_permission'].push(response.data.data);
        // getObjectLevelPermissions();/
        commonDataShare.closeModal('#createObjectLevelPermissionModal');
        swal(constants.name, constants.create_success,constants.success);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    // $scope.updateObjectLevelPermission = function(){
    //   cfpLoadingBar.start();
    //   cfpLoadingBar.inc();
    //   userService.updateObjectLevelPermission()
    //   .then(function onSuccess(response){
    //     console.log(response);
    //     cfpLoadingBar.complete();
    //   }).catch(function onError(response){
    //     console.log(response);
    //   })
    // }
    $scope.assignObjectName = function(c){
      console.log(c);
    }
    //genral user level permissions
    var getGeneralUserLevelPermissions = function()
    {
      userService.getGeneralUserLevelPermissions()
      .then(function onSuccess(response){
        console.log(response);
        $scope.generalUserLevelPermissionsList = response.data.data;
      }).catch(function onError(response){
        console.log(response);
      })
    }

    $scope.createGeneralUserLevelPermission = function(){
      console.log($scope.generalUserLevelPermissionData);
      userService.createGeneralUserLevelPermission($scope.generalUserLevelPermissionData)
      .then(function onSuccess(response){
        console.log(response);
        console.log("hello" + $scope.profileData);
        commonDataShare.closeModal('#createGeneralUserPermissionModal');
        // getGeneralUserLevelPermissions();
        if(!$scope.profileData.general_user_permission)
          $scope.profileData['general_user_permission'] = [];
        $scope.profileData['general_user_permission'].push(response.data.data);
        swal(constants.name, constants.create_success, constants.success);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    $scope.setModalData = function(data){
      console.log(data);
      $scope.modalData = data;
    }
    // start : update object and general user level permission
    $scope.updateObjectLevelPermission = function(permission,index){
      $scope.isDataUpdating = true;
      cfpLoadingBar.start();
      userService.updateObjectLevelPermission(permission)
      .then(function onSuccess(response){
        console.log(response);
        cfpLoadingBar.complete();
        $scope.isDataUpdating = false;
        $scope.profileData.object_level_permission[index] = response.data.data;
      }).catch(function onError(response){
        console.log(response);
        $scope.isDataUpdating = false;
      })
    }
    $scope.updateGeneralUserPermission = function(permission,index){
      $scope.isDataUpdating = true;
      cfpLoadingBar.start();
      userService.updateGeneralUserPermission(permission)
      .then(function onSuccess(response){
        console.log(response);
        cfpLoadingBar.complete();
        $scope.isDataUpdating = false;
        $scope.profileData.general_user_permission[index] = response.data.data;
      }).catch(function onError(response){
        console.log(response);
        $scope.isDataUpdating = false;
      })

    }
    // end : update object and general user level permission
    //start:onboard functionality
    $scope.activityNumber = 1;
    $scope.createOnBoardActivity = function(number){
      if(number == 1 && $scope.organisationData.name && $scope.organisationData.phone && $scope.organisationData.email && $scope.organisationData.category){
        console.log("org");
        $scope.createOrganisation();
        console.log($scope.onBoardOrgId);
        $scope.activityNumber++;
      }
      if(number == 2 && $scope.profileData.name && $scope.cloneFromProfileId.id){
        $scope.cloneProfileGeneral($scope.cloneFromProfileId.id, $scope.onBoardOrgId, $scope.profileData.name);
      }
    }
    // use this function to clone a profile within an organisation
    $scope.cloneProfileGeneral = function(cloneFromProfileId, onBoardOrgId, profileNewName){

      console.log("cloneProfileGeneral", cloneFromProfileId, onBoardOrgId, profileNewName);

      var data = {
        clone_from_profile_id : cloneFromProfileId,
        new_organisation_id : onBoardOrgId,
        new_name : profileNewName ,
      }
      userService.cloneProfile(data)
      .then(function onSuccess(response){
        console.log("cloned",response);
        $scope.clonedProfileId = response.data.data.id;
        $scope.getProfiles();
        commonDataShare.closeModal('#cloneProfileModal');
        swal(constants.name, constants.create_success, constants.success);
      }).catch(function onError(response){
        console.log(response);
        swal(constants.name, constants.errorMsg, constants.error);
      })

    }

    $scope.validateOnBoardData = function(activity){
      if(activity == 'finish'){
        if($scope.model.firstname && $scope.model.lastname && $scope.model.username && $scope.model.email && $scope.model.password)
          return false;
        else
          return true;
      }
    }
    $scope.getOrganisationsByCategory = function(category,source){
      userService.getOrganisationsByCategory(category)
      .then(function onSuccess(response){
        console.log("categoryOrg",response);
        if(source)
          $scope.sourceOrganisationListByCategory = response.data.data;
        else
          $scope.destinationOrganisationListByCategory = response.data.data;
      }).catch(function onError(response){
        console.log(response);
      })
    }
    $scope.createOrganisationMapping = function(){
      console.log($scope.mappingData);
      userService.createOrganisationMapping($scope.mappingData)
      .then(function onSuccess(response){
        console.log(response);
        commonDataShare.closeModal('#createNewOrganisationMapModal');
        $scope.organisationMappingList.push(response.data.data);
        swal(constants.name,constants.create_success,constants.success);
      }).catch(function onError(response){
          console.log(response);
          swal(constants.name,constants.errorMsg,constants.error);
      })
    }
    var getOrganisationMappingList = function(organisationId){
      userService.getOrganisationMappingList(organisationId)
      .then(function onSuccess(response){
        console.log(response);
        $scope.organisationMappingList = response.data.data;
      }).catch(function onError(response){
        console.log(response);
      })
    }
   }]);//end of controller
