"use strict";
angular.module('catalogueApp')
    .controller('LeadFormCtrl', function($scope, $rootScope, $stateParams, $window, $location, LeadFormService ,$http, constants, permissions, commonDataShare) {
      console.log("hello");
      var fieldType = {
        firstname1 : 'text',
        lastname1 : 'text',
        firstname2 : 'text',
        lastname2 : 'text',
        mobile1 : 'number',
        mobile2 : 'number',
        email1 : 'email',
        email2 : 'email',
        address : 'text',
        alphanumeric1 : 'text',
        alphanumeric2 : 'text',
        alphanumeric3 : 'text',
        alphanumeric4 : 'text',
        boolean1 : 'radio',
        boolean2 : 'radio',
        boolean3 : 'radio',
        boolean4 : 'radio',
        float1 : 'number',
        float2 : 'number',
        date1 : 'date',
        date2 : 'date',
        is_interested : 'radio'
      };
      $scope.modelData = {};
      var getCampaignLeadAliasData = function(campaignId){
        LeadFormService.getCampaignLeadAliasData(campaignId)
        .then(function onSuccess(response){
          console.log(response);
          $scope.alias_data = response.data.data;
        }).catch(function onError(response){
          console.log(response);
        })
      }
      var campaignId = $stateParams.campaignId;
      var supplierId = $stateParams.supplierId;
      getCampaignLeadAliasData(campaignId);

      $scope.getFieldType = function(field){
        return fieldType[field];
      }
      $scope.checkValidFields = function(field){
        if (field == 'boolean1' || field == 'boolean2' || field == 'boolean3' || field == 'boolean4' || field == 'is_interested')
          return false;
        else
          return true;
      }

      var getCampaignInfo = function(campaignId){
        LeadFormService.getCampaignInfo(campaignId)
        .then(function onSuccess(response){
          console.log(response);
          $scope.proposalInfo = response.data.data;
        }).catch(function onError(response){
          console.log(response);
        })
      }
      getCampaignInfo(campaignId);
      var supplierId = $stateParams.supplierId;
      var getSupplierDetails = function(supplierId){
        LeadFormService.getSupplierDetails(supplierId)
        .then(function onSuccess(response){
          console.log(response);
          $scope.supplierInfo = response.data.society_data;
        }).catch(function onError(response){
          console.log(response);
        })
      }
      getSupplierDetails(supplierId);
      var supplierCode = $stateParams.supplierCode;0
      $scope.saveLeads = function(){
        $scope.modelData['campaign'] = campaignId;
        $scope.modelData['object_id'] = supplierId;
        var data = {
          'lead_data' : $scope.modelData,
          'supplierCode' : supplierCode
        }
        $scope.modelData['supplierCode'] = supplierCode;
        console.log(data);
        LeadFormService.saveLeads(data)
        .then(function onSuccess(response){
          console.log(response);
          $scope.modelData = {};
          swal(constants.name,constants.save_success,constants.success);
        }).catch(function onError(response){
          console.log(response);
        })
      }

      $scope.getLeads = function(){
        LeadFormService.getLeads(campaignId,supplierId)
        .then(function onSuccess(response){
          console.log(response);
          $scope.showLeads = true;
          $scope.leadsData = response.data.data;
        }).catch(function onError(response){
          console.log(response);
        })
      }

      $scope.changeView = function(){
        $scope.showLeads = false;
      };

      $scope.editView = function(lead){
         $scope.showLeads = false;
         $scope.modelData = lead;
         $scope.editLead = true;
      }
      $scope.updateLeads = function(){
        LeadFormService.updateLeads($scope.modelData.id,$scope.modelData)
        .then(function onSuccess(response){
          console.log(response);
          $scope.getLeads();
        }).catch(function onError(response){
          console.log(response);
        })
      }

    });
