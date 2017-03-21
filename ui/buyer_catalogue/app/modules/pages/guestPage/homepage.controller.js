angular.module('machadaloPages')
.controller('guestHomePageController',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService','constants','createProposalService','pagesService',
    function ($scope, $rootScope, $window, $location, pagesService, constants, createProposalService,pagesService) {
      var $jq = jQuery.noConflict();
      var $jp = jQuery.noConflict();
      $scope.model = {};
      $scope.proposalRequest = {};
      $scope.address = {};
      $scope.supplier_codes = [
        {name:'Society', code:'RS'},
        {name:'Corporate Park', code:'CP'},
      ];
      $scope.supplier_type_code = {
        code:'',
      };

      $scope.model['business'] = {};
      $jq(document).ready(function(){
        $('.campaignCarousel').slick({
         slidesToShow: 4,
         slidesToScroll: 1,
         autoplay: true,
         autoplaySpeed: 1000,
        });
      });
      $jp(document).ready(function(){
        $('.spaceCarousel').slick({
          // prevArrow : ' <img src="img/cleft.png"></img>',
          // nextArrow : '<img src="img/cright.png"></img>',
           slidesToShow: 3,
           slidesToScroll: 1,
           autoplay: true,
           autoplaySpeed: 1000,
        });
      });
      //To load cities
      createProposalService.loadInitialData()
        .then(function onSuccess(response){
          console.log(response);
            $scope.cities = response.data.cities;
          })
          .catch(function onError(response){
            console.log("Error in load cities");
          });
        //To load business types
        $scope.bus_type_id;
      pagesService.loadBusinessTypes()
      .then(function onSuccess(response){
        console.log(response);
          $scope.businessTypes = response.data;
        })
        .catch(function onError(response){
          // swal(constants.name,constants.errorMsg,constants.error);
          console.log("Error in load busieness types");
        });
      //To load business subtypes
      $scope.locality;
      $scope.getSubTypes = function(id) {
        console.log(componentForm);
        console.log("hello",id,$scope.bus_type_id);
        // var id = $scope.model.business.business_type_id;
        pagesService.getSubTypes(id)
          .then(function onSuccess(response){
            console.log(response);
            $scope.business_subtypes = response.data;
        })
        .catch(function onError(response){
          console.log("Error Occured in loading business subtypes");
        });
      }
      //To get location
      var componentForm = {
        street_number: 'short_name',
        route: 'long_name',
        locality: 'long_name',
        administrative_area_level_1: 'short_name',
        country: 'long_name',
        postal_code: 'short_name',
        sublocality_level_1 : 'short_name',
        natural_feature : 'short_name',
      };
      $scope.$on('place_changed', function (e, place) {
        $scope.address = {};
          // do something with place
        console.log(place.address_components);
        for (var i = 0; i < place.address_components.length; i++) {
         var addressType = place.address_components[i].types[0];
         if (componentForm[addressType]) {
           var val = place.address_components[i][componentForm[addressType]];
           $scope.address[addressType] = val;
           console.log(val);
         }
       }
       try{
         $scope.proposalRequest = {
           centers : [{
             center : {
               area : $scope.address.sublocality_level_1,
               subarea : $scope.address.natural_feature || $scope.address.sublocality_level_1,
               address : $scope.address.sublocality_level_1,
               pincode : $scope.address.postal_code||'',
               city : $scope.address.locality,
               center_name : $scope.address.sublocality_level_1,
               radius : '2',
               codes : [],
             },
           }],
         };
       }catch(error){
         swal(constants.name,constants.location_error,constants.error);
       }
      });
      //To create business,account and proposal_id
      $scope.create = function(){
        // $scope.model.business.name="MyBusiness";
        $scope.model.business.name = calculateBusinessName();
        $scope.model.business['contacts'] = {};
        console.log($scope.model);
        pagesService.createBusinessCampaign($scope.model)
          .then(function onSuccess(response) {
            $scope.model = response.data;
            $scope.business_id = response.data.business.business_id;

            $scope.model['account'] = {};
            $scope.model.account['business_id'] = $scope.model.business.business_id;
            $scope.model.account['contacts'] = {};
            // $scope.model.account.name = "MyAccount";
            $scope.model.account.name = calculateAccountName();
            pagesService.createAccountCampaign($scope.model)
            .then(function onSuccess(response) {
              console.log(response);
              $scope.account_id = response.data.account.account_id;
              $scope.proposalRequest.business_id = $scope.business_id;
              $scope.proposalRequest.centers[0].center.codes.push($scope.supplier_type_code.code);
              console.log($scope.proposalRequest);
              createProposalService.saveInitialProposal($scope.account_id, $scope.proposalRequest)
              .then(function onSuccess(response){
                $location.path('/' + response.data.data + '/mapview');
                console.log(response);
              }).catch(function onError(response){
                console.log("Error in creating proposal");
              })
            })
            .catch(function onError(response){
              console.log(response);
            });

            console.log(response);
          }).catch(function onError(response){
            console.log(response);
          });
      }
      var calculateBusinessName = function(){
        console.log($rootScope);
        var name = $rootScope.globals.currentUser.name + 'business' + Math.random().toString(36).substring(2, 8);
        return name;
      }
      var calculateAccountName = function(){
        console.log($rootScope);
        var name = $rootScope.globals.currentUser.name + 'account' + Math.random().toString(36).substring(2, 8);
        return name;
      }


}]);//end of controller
