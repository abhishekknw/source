angular.module('machadaloPages')
.controller('CreateAccountCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService','constants','$stateParams','commonDataShare',
    function ($scope, $rootScope, $window, $location, pagesService, constants, $stateParams, commonDataShare) {
      $scope.model = {};
      $scope.model.account = {};
      $scope.organisationData = {};
    	$scope.accounts = [];

      $scope.organisationData = JSON.parse($window.localStorage.organisationInfo);
      console.log($scope.organisationData);


      $scope.contact = {
        name: '',
        designation: '',
        department: '',
        email: '',
        mobile: undefined,
        spoc: ''
      };

      var contactCopy = angular.copy($scope.contact);
      $scope.model.account.contacts = [$scope.contact];


      $scope.addNew = function() {
        // object def is directly added to avoid different array elements pointing to same object
        $scope.setContact=false;
        $scope.model.account.contacts.push({
        name: '',     designation: '',    department: '',
        email: '',    mobile: undefined,      spoc: ''
      });


      };


       $scope.remove = function(index) {
        $scope.model.account.contacts.splice(index, 1);
      };


      $scope.updatefields = function(){
        if ($scope.model.account.business_id == ""){
          $scope.business_type = "";
          $scope.business_sub_type = "";
        }else{

        }
      }


      var accId = pagesService.getAccountId();
      if($stateParams.accountId){
        $scope.selectAcc = $stateParams.accountId;
        // $scope.getAccount();
      }
      // else{
      //   // $scope.model.business = pagesService.getBusinessObject();
      //   $scope.model.business = JSON.parse($window.localStorage.business);
      //   $scope.model.account.business_id = $scope.model.business.business_id;
      // }

      $scope.readMore = function() {
              $scope.seeMore = "true";
      };

      $scope.editDetails = function() {
              $scope.choice = "select";
      };

      $scope.newAccount = function() {
              $scope.choice = "new";
              $scope.selectAcc = undefined;
        // complete object definition given to avoid multiple refrence to same field
              $scope.contact = {
                name: '',
                designation: '',
                department: '',
                email: '',
                mobile: undefined,
                spoc: ''
              };

              $scope.form.$setPristine();
              $scope.model.account = {};
              $scope.model.account.contacts = [$scope.contact];
      };

      //Code for Automatically select createAccount from business account details
      $scope.setAccount == false;
      $scope.setCreate_Account = function(){
        if($scope.setAccount == true){
          console.log($scope.model);
        $scope.model.account.name = $scope.model.business.contacts[0].name;;
        $scope.model.account.email = $scope.model.business.email;
        $scope.model.account.phone = $scope.model.business.phone;
        $scope.model.account.address = $scope.model.business.address;
        $scope.model.account.reference_name= $scope.model.business.reference_name;
        $scope.model.account.reference_phone = $scope.model.business.reference_phone;
        $scope.model.account.reference_email= $scope.model.business.reference_email;
        $scope.setAccount == true;
      }else{
        $scope.model.account.name = "";
        $scope.model.account.email = "";
        $scope.model.account.phone = "";
        $scope.model.account.address = "";
        $scope.model.account.reference_name= "";
        $scope.model.account.reference_phone = "";
        $scope.model.account.reference_email= "";
        $scope.setAccount == false;
      }
    };
      // Code for Automatically select Account Contact from Business Account
      $scope.setContact=false;
      $scope.setContact_Account = function(index){
        if($scope.setContact == false){
        $scope.model.account.contacts[index].name = $scope.model.business.contacts[0].name;
        $scope.model.account.contacts[index].designation = $scope.model.business.contacts[0].designation;
        $scope.model.account.contacts[index].department = $scope.model.business.contacts[0].department;
        $scope.model.account.contacts[index].email = $scope.model.business.contacts[0].email;
        $scope.model.account.contacts[index].mobile = $scope.model.business.contacts[0].mobile;

        $scope.setContact=true;
      }else{
        $scope.model.account.contacts[index].name = "";
        $scope.model.account.contacts[index].designation = "";
        $scope.model.account.contacts[index].department = "";
        $scope.model.account.contacts[index].email = "";
        $scope.model.account.contacts[index].mobile = undefined;
        $scope.setContact=false;
      }
    };


        //after adding organisation instead of business
        var organisationId = $stateParams.organisationId;
        var getOrganisation = function(){
          pagesService.getOrganisation(organisationId)
          .then(function onSuccess(response){
            console.log(response);
            $scope.organisationData = response.data.data;
          }).catch(function onError(response){
            console.log(response);
            commonDataShare.checkPermission(response);
          })
        }
        $scope.createAccount = function(){
          console.log($scope.model);
          $scope.model.account['organisation'] = $scope.organisationData.organisation_id;
          pagesService.createAccount($scope.model.account)
          .then(function onSuccess(response){
            console.log(response);
            swal(constants.name, constants.create_success, constants.success);
            $location.path("/manageCampaign/create");
          }).catch(function onError(response){
            console.log(response);
            commonDataShare.checkPermission(response);
          })
        }
        var accountId = $stateParams.accountId;
        var getAccount = function(){
          pagesService.getAccount(accountId)
          .then(function onSuccess(response){
            console.log(response);
            $scope.model.account = response.data.data.account;
            $scope.model.account.contacts = response.data.data.contacts;
            $scope.organisationData['name'] = $window.localStorage.organisation_name;
          }).catch(function onError(response){
            console.log(response);
            commonDataShare.checkPermission(response);
          })
        }
        if(accountId){
          $scope.editAccountField = true;
          getAccount();
        }
        $scope.editAccount = function(){
          pagesService.editAccount($scope.model.account,accountId)
          .then(function onSuccess(response){
            console.log(response);
            swal(constants.name, constants.update_success, constants.success);
          }).catch(function onError(response){
            console.log(response);
          })
        }


    }]);
