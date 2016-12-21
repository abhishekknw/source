angular.module('machadaloPages')
.controller('CreateAccountCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {
      $scope.model = {};
      $scope.model.account = {};
    	$scope.accounts = [];
      $scope.supplier_types = ['Society', 'Corporate', 'Club', 'Mall', 'School/College']
    	$scope.campaign_types = ['Poster', 'Standee', 'Stall', 'CarDisplay', 'Fliers']
    	$scope.campaign_sub_types = {
    		'Poster': ['A4', 'A3'],
    		'Standee': ['Small', 'Medium', 'Large'],
    		'Stall':['Small', 'Medium', 'Large','Canopy'],
    		'CarDisplay':['Normal', 'Premium'],
            'Fliers': ['Normal']
    	}

        $scope.clear = function() {
        $scope.dt = null;
      };

      $scope.maxDate = new Date(2020, 5, 22);
      $scope.today = new Date();
      $scope.popup1 = false;
      $scope.popup2 = false;

      $scope.setDate = function(year, month, day) {
        $scope.dt = new Date(year, month, day);
      };

      $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
      };

      $scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
      $scope.format = $scope.formats[1];
      $scope.altInputFormats = ['M!/d!/yyyy'];

      //$scope.phoneNumberPattern = /^[1-9]{1}[0-9]{9}$/
    	$scope.campaign_type = {}

      $scope.contact = {
        name: '',
        designation: '',
        department: '',
        email: '',
        phone: '',
        spoc: ''
      };

      var contactCopy = angular.copy($scope.contact);
      $scope.model.account.contacts = [$scope.contact];

      // pagesService.getAllBusinesses()
      //   .success(function (response, status) {
      //         console.log("Get All Business response : ");
      //         console.log(response);
      //         $scope.businesses = response;
      //    });

      // pagesService.loadBusinessTypes()
      // .success(function (response){
      //     $scope.busTypes = response;
      //   });

        // $scope.getSubTypes = function() {
        //   var id = $scope.model.business.type;
        //   pagesService.getSubTypes(id)
        //   .success(function (response){
        //       $scope.sub_types = response;
        //     });
        // }


      $scope.addNew = function() {
        // object def is directly added to avoid different array elements pointing to same object
        $scope.setContact=false;
        $scope.model.account.contacts.push({
        name: '',     designation: '',    department: '',
        email: '',    phone: '',      spoc: ''
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

    	// $scope.getAllAccounts = function() {
     //    $scope.selectAcc = undefined;
	    // 	pagesService.getAllAccounts()
	    // 	.success(function (response, status) {
	    // 		    console.log(response);
	    //         $scope.accounts = response;
	    //    });
	    // };

    	$scope.getAccount = function() {
    		pagesService.getAccount($scope.selectAcc)
	    	.success(function (response, status) {
	            $scope.model.account = response.account;
              $scope.model.business = response.business;
              $scope.model.business.contacts = response.business.contacts;
              $scope.model.account.business_id = response.business.business_id.toString();
	            $scope.choice = "selected";
	       });
      };

      var accId = pagesService.getAccountId();
      if(accId){
        $scope.selectAcc = accId;
        $scope.getAccount();
      }
      else{
        // $scope.model.business = pagesService.getBusinessObject();
        $scope.model.business = JSON.parse($window.sessionStorage.business);
        $scope.model.account.business_id = $scope.model.business.business_id;
      }

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
                phone: '',
                spoc: ''
              };

              $scope.form.$setPristine();
              $scope.model.account = {};
              $scope.model.account.contacts = [$scope.contact];
      };


      // $scope.resetValues = function(){
      //           $scope.model.campaign_type = undefined;
      //           $scope.model.tentative = undefined;
      //           $scope.supplier_type = undefined;
      //           $scope.campaign_type1 = undefined;
      //           $scope.supplier_type1 = undefined;

      // }

      //Code for Automatically select createAccount from business account details
      $scope.setAccount == false;
      $scope.setCreate_Account = function(){
        if($scope.setAccount == true){
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
        $scope.model.account.contacts[index].phone = $scope.model.business.contacts[0].phone;

        $scope.setContact=true;
      }else{
        $scope.model.account.contacts[index].name = "";
        $scope.model.account.contacts[index].designation = "";
        $scope.model.account.contacts[index].department = "";
        $scope.model.account.contacts[index].email = "";
        $scope.model.account.contacts[index].phone = "";
        $scope.setContact=false;
      }
    };



    	$scope.create = function() {
            pagesService.createAccountCampaign($scope.model)
            .success(function (response, status) {

              console.log("\n\nresponse is : ");

              var business_id = $scope.model.account.business_id

              if (status == '200'){
                pagesService.setBusinessId(business_id);
                $scope.model.account = response.account;
                $scope.model.account.contacts = response.contacts;
                $scope.model.account.business_id = business_id;
                $location.path("/manageCampaign/create");
                $scope.successMsg = "Successfully Saved"
                $scope.errorMsg = undefined;
                $scope.choice = "selected";

              }
          }).error(function(response, status){

            // status = 406 comes from backend if some information is missing with info in response.message
             // response = response ? JSON.parse(response) : {}
             // console.log(response.message);
             // $scope.successMsg = undefined;
             // $scope.errorMsg = response.message ;
             // console.log(status);
             if (typeof response != 'number'){
               $scope.successMsg = undefined;
               $scope.errorMsg = response.message;
               console.log($scope.errorMsg);
            }

        })
        };
    }]);
