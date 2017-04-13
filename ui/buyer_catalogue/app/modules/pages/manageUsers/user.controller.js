angular.module('machadaloPages')
.controller('userCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'userService','constants','$timeout',
    function ($scope, $rootScope, $window, $location, userService, constants, $timeout) {
        // reset login status
     $scope.model = {};
     $scope.permissionList = [];
     $scope.groupName = {};
     $scope.selectedGroupList = [];
     $scope.passwordError = constants.password_error;
     $scope.options = [
        {usercode : 'BD', id : '01'},
        {usercode : 'Ops', id: '02'},
        {usercode : 'Agency', id: '03'}
      ];

      //To get permission list
      userService.getAllUserPermissions()
      .then(function onSuccess(response){
        console.log(response);
        $scope.permissions = response.data.data;
        addMoreFieldsToPermission();
        })
        .catch(function onError(response){
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
        swal(constants.name,constants.createUser,constants.success);
        // alert("Successfully Created");
        })
        .catch(function onError(response){
            console.log("error occured");
            swal(constants.name,constants.errorMsg,constants.error);
            // alert("Error Occured");
        });
     }
     $scope.menuItem = [
       {name : 'createUser'},
       {name : 'createGroup'},
     ];
     $scope.contentItem = {
       createUser : 'createUser',
       createGroup : 'createGroup',
     }
     $scope.getContent = function(item){
       console.log(item);
       $scope.menuItem.name = item;
     }
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
         swal(constants.name,constants.create_group_error,constants.error);
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
   }]);//end of controller
