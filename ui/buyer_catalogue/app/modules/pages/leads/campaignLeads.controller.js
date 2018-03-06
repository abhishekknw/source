"use strict";
angular.module('catalogueApp')
    .controller('CampaignLeadsCtrl', function($scope, $rootScope, $stateParams, $window, $location, campaignLeadsService ,$http, constants, permissions, commonDataShare) {
      $scope.modelData = {};
      $scope.modelData['alias_data'] = [];
      $scope.savedFormFields = [];
      console.log("hello");
      $scope.campaignHeaders = [
        {header : 'Campaign Name'},
        {header : 'Start Date'},
        {header : 'End Date'},
        {header : 'Action'},
        {header : 'Action'},
        {header : 'Action'},
      ];
      var formFieldsStruct = [
        {name : 'firstname1' , value : false},
        {name : 'lastname1' , value : false},
        {name : 'firstname2' , value : false},
        {name : 'lastname2' , value : false},
        {name : 'mobile1' , value : false},
        {name : 'mobile2' , value : false},
        {name : 'phone' , value : false},
        {name : 'email1' , value : false},
        {name : 'email2' , value : false},
        {name : 'address' , value : false},
        {name : 'alphanumeric1', value : false},
        {name : 'alphanumeric2', value : false},
        {name : 'boolean1', value : false},
        {name : 'boolean2', value : false},
      ];
      $scope.formFields = angular.copy(formFieldsStruct);
      $scope.views = {
        viewLeads : false,
        createForm : false,
        campaigns : true,
        addLeads : false,
      }
      $scope.create = function(){
        $scope.modelData['campaign'] = $scope.campaignId;
        console.log($scope.modelData);
        campaignLeadsService.create($scope.modelData)
        .then(function onSuccess(response){
          console.log(response);
        }).catch(function onError(response){
          console.log(response);
        })
      }
      //checkSavedFields function is used to disable selected fields in dropdown ui of formFields
      var checkSavedFields = function(){
        angular.forEach($scope.modelData.alias_data, function(field){
          $scope.savedFormFields[field.original_name] = field;
        })
      }

      campaignLeadsService.getLeads('LODLODCA10')
      .then(function onSuccess(response){
        console.log(response);
        $scope.leadsData = response.data.data;
      }).catch(function onError(response){
        console.log(response);
      })
      $scope.addField = function(){
        var data = {
          alias : '',
          original_name : ''
        }
        $scope.modelData.alias_data.push(data);
        checkSavedFields();
      }
      var assigned_by = '0';
      var fetch_all = '0';
      var userId = $rootScope.globals.currentUser.user_id;
      campaignLeadsService.getCampaignDetails(assigned_by,userId,fetch_all)
        .then(function onSuccess(response){
          console.log(response);
          $scope.campaigns = response.data.data;
        })
        .catch(function onError(response){
          console.log(response);
        });
      $scope.addField();
      $scope.changeView = function(view,campaign){
        $scope.views = {
          createForm : false,
          viewLeads : false,
          campaigns : false,
          addLeads : false,
        }
        $scope.views[view] = true;
        console.log(view,$scope.views.createForm);
        switch(true){
          case $scope.views.createForm:
            $scope.campaignId = campaign.campaign.proposal_id;
            getCampaignLeadAliasData($scope.campaignId);
            console.log($scope.campaignId);
            break;
        }
      }
      var getCampaignLeadAliasData = function(campaignId){
        campaignLeadsService.getCampaignLeadAliasData(campaignId)
        .then(function onSuccess(response){
          console.log(response,$scope.modelData);
          $scope.modelData.alias_data = response.data.data;
          checkSavedFields();

        }).catch(function onError(response){
          console.log(response);
        })
      }
    });//Controller ends here
