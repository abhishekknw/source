angular.module('machadaloPages')
.controller('userCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'userService','constants','$timeout',
    function ($scope, $rootScope, $window, $location, userService, constants, $timeout) {
        // reset login status
     $scope.model = {};
     $scope.permissionList = [];
     $scope.groupName = {};
     $scope.selectedGroupList = [];
     $scope.permissionsDict = [];
     $scope.userInfo = {};
     $scope.passwordError = constants.password_error;
     $scope.profileData = {};// to create profile
     $scope.organisationData = {}; // to create organisation
     $scope.organisationMappedIdList = []; // to create a list of organisation ids
     $scope.options = [
        {usercode : 'BD', id : '01'},
        {usercode : 'Ops', id: '02'},
        {usercode : 'Agency', id: '03'}
      ];

    $scope.userInfoHeaders = [
      {header : 'First Name'},
      {header : 'Last Name'},
      {header : 'Email Id'},
      {header : 'Username'},
      {header : 'Groups'},
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
      //calling when page load
      getAllUserGroups();
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
     $scope.register = function(){
       $scope.model['groups'] = $scope.selectedGroupList;
       console.log($scope.model);
     userService.createUser($scope.model)
      .then(function onSuccess(response){
        console.log("Successful");
        $scope.selectedGroupList = [];
        $scope.model = {};
        addMoreFieldsToGroup();
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
     }
     $scope.getContent = function(item,data){
       console.log(item);
       $scope.menuItem.name = item;
        switch(item){
          case $scope.contentItem.viewUsers:
            getAllUsers();
            addMoreFieldsToGroup();
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
            getProfiles();
            getOrganisations();
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
        $('#passwordModal').modal('hide');
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
      userService.createOrganisation($scope.organisationData)
      .then(function onSuccess(response){
        console.log(response);
        swal(constants.name,constants.create_success,constants.success);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    //end: create organisation
    var getOrganisations = function(){
      userService.getOrganisations()
      .then(function onSuccess(response){
        $scope.organisationList = response.data.data;
        angular.forEach($scope.organisationList, function(organisation){
          console.log(organisation);
          $scope.organisationMappedIdList[organisation.organisation_id] = organisation;
        })
        console.log(response);
      }).catch(function onError(response){
        console.log(response);
      })
    }
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
      // console.log(data);
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
        swal(constants.name,constants.create_success,constants.success);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    //end: create profile
    var getProfiles = function(){
      userService.getProfiles()
      .then(function onSuccess(response){
        $scope.profilesList = response.data.data;
        console.log(response);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    $scope.goToProfiles = function(contentItem, operation, data={}){
      $scope.profileData = data;
      $scope.operationProfile.view = false;
      $scope.operationProfile.create = false;
      $scope.operationProfile.edit = false;
      $scope.operationProfile[operation] = true;
      console.log($scope.profileData);
      $scope.getContent(contentItem);
    }
    $scope.updateProfile = function(){
      userService.updateProfile($scope.profileData)
      .then(function onSuccess(response){
        console.log(response);
        swal(constants.name,constants.update_success,constants.success);
      }).catch(function onError(response){
        console.log(response);
      })
    }
   }]);//end of controller
