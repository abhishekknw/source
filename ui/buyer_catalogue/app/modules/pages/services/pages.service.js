'use strict';

/**
 * @ngdoc service
 * @name mdopsApp.societyDetailsService
 * @description
 * # societyDetailsService
 * Service in the mdopsApp.
 */

angular.module('machadaloPages').factory('pagesService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

   var url_base = "v0/ui/website/";
   var pagesService = {};
   var business_id = undefined;
   var account_id = undefined;
   var business = undefined;
   var proposal_accountId = undefined;

   pagesService.setBusinessObject = function(business_received){
      business = business_received;
   }

   pagesService.getBusinessObject = function(){
      return business;
   }

   pagesService.setBusinessId = function(id){
      business_id = id;
   }

   pagesService.getProposalAccountId = function(){
     return proposal_accountId;
   }

   pagesService.setProposalAccountId = function(id){
      proposal_accountId = id;
   }

   pagesService.getBusinessId = function(){
     return business_id;
   }

   pagesService.setAccountId = function(id){
    account_id  =id;
   }

   pagesService.getAccountId = function(){
    return account_id;
   }

   // To return the archived estimates
   pagesService.listSocieties = function (sObj) {
     var url = url_base + "society/list/";
     if(sObj && sObj != "")
      url += "?search="+sObj
     return machadaloHttp.get(url);
   };

  //   pagesService.getAllBusinesses = function () {
  //     var url = url_base + "businesses/";
  //     return machadaloHttp.get(url);
  //  };

  pagesService.getOrganisations = function (id) {
    var url = url_base + "organisation-map/?source_organisation_id=" + id;
    return machadaloHttp.get(url);
 };


   pagesService.getBusiness = function (id) {
       var url = url_base + "business/" + id;
       return machadaloHttp.get(url);
      };

  pagesService.getAllAccounts = function () {
      var url = url_base + "accounts/";
      return machadaloHttp.get(url);
    };

  //  pagesService.getAccount = function (id) {
  //     var url = url_base + "account/" + id;
  //     return machadaloHttp.get(url);
  //  };

  pagesService.loadBusinessTypes = function () {
      var url = url_base + "create_business/load_business_types/";
      return machadaloHttp.get(url);
  };

  pagesService.getSubTypes = function (id) {
      var url = url_base + "subtypes/" + id + "/";
      return machadaloHttp.get(url);
  };

    // pagesService.createBusinessCampaign = function (data) {
    //    var url = url_base + "newCampaign/";
    //    return machadaloHttp.post(url, data);
    //   };

    pagesService.createAccountCampaign = function (data) {
       var url = url_base + "newAccountCampaign/";
       return machadaloHttp.post(url, data);
    };

    pagesService.getCampaigns = function (status) {
       var url = url_base + "getCampaigns/?status=" + status;
       return machadaloHttp.get(url);
      };


    pagesService.saveFinalizedInventory = function (data) {
      var url = url_base + "campaign/" + data.inventory[0].inventories[0].campaign + "/inventories/";
      return machadaloHttp.post(url, data);
    };

    pagesService.getSocietyInventory = function (id) {
       var url = url_base + "campaign/" + id + "/inventories/";//The id here referes to campaign id
       return machadaloHttp.get(url);
      };

    pagesService.removeThisSociety = function(society_id, type) {
      var url = url_base + "campaign/" + society_id + "/inventories/?type=" + type; //The id here referes to societybooking id to be deleted, not campaign id
      return machadaloHttp.delete(url);
     }

     pagesService.book = function (campaign_id, new_status) {
      var url = url_base + "campaign/" + campaign_id+ "/book/?status=" + new_status;
      return machadaloHttp.get(url);
    };

    pagesService.getAccountProposal = function(account_id){
      //  var url = url_base + account_id + '/getAccountProposals/';
      //hitting other Api which filters only parent proposals if account_id is provided
      var url = url_base + "child-proposals/0/?account_id=" + account_id;
       return machadaloHttp.get(url);
    }

    pagesService.processParam = function(){
     if($stateParams.campaignId){
       $rootScope.campaignId = $stateParams.campaignId;
     }else {
       $rootScope.campaignId = null;
     }
     if($stateParams.societyId){
      $rootScope.societyId = $stateParams.societyId;
     }else{
      $rootScope.societyId = null;
    }
   };
   pagesService.createOrganisation = function (data) {
      var url = url_base + "organisation/";
      return machadaloHttp.post(url, data);
     };

    pagesService.getOrganisation = function(id){
      var url = url_base + "organisation/" + id + "/";
      return machadaloHttp.get(url);
    }

    pagesService.getAccounts = function(id){
      var url = url_base + "account/?organisation_id=" + id;
      return machadaloHttp.get(url);
    }

    pagesService.getAccount = function (id) {
       var url = url_base + "account/" + id;
       return machadaloHttp.get(url);
    };

   return pagesService;
}]);
