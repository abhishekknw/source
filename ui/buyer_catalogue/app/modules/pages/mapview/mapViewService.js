 'use strict';
 angular.module('catalogueApp')
 .factory('mapViewService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

    var url_base = 'v0/ui/website/';
    var mapViewService = {};
    var url_base_societyDetails ='v0/ui/';

    mapViewService.getSpaces = function(proposal_id){
        var url = url_base + "proposal/"+ proposal_id + "/get_spaces/";
        return machadaloHttp.post(url, {});
    };

    mapViewService.getChangedCenterSpaces = function(proposal_id, data){
        // done
        var url = url_base + "proposal/"+ proposal_id + "/get_spaces/";
        return machadaloHttp.post(url,data);
    };

    mapViewService.resetCenter = function(proposal_id, data){
        // done
        var url = url_base + "proposal/"+ proposal_id + "/get_spaces/";
        return machadaloHttp.post(url,data);
    }

    mapViewService.getFilterSocieties = function(get_data){
        var url = url_base + 'getFilteredSocieties/' + get_data;
        return machadaloHttp.get(url);
    }

    //added to get supplier filters like for RS,CP...etc
    mapViewService.getFilterSuppliers = function(supplier_data){
        var url = url_base + 'filtered-suppliers/';
        return machadaloHttp.post(url,supplier_data);
    }

    //added to search suppliers based on supplier code and search text
    mapViewService.searchSuppliers = function(code,searchtext){
        var url = url_base + 'supplier-search/?' + "search=" + searchtext + "&supplier_type_code=" + code ;
        return machadaloHttp.get(url);
    }

    mapViewService.saveData = function(proposal_id, centers_data){
        var url = url_base + proposal_id + '/create-final-proposal/';
        return machadaloHttp.post(url, centers_data);
    }

    mapViewService.exportProposalData = function(proposal_id, centers_data){
        var url = url_base + proposal_id + '/proposal-version/';
        return machadaloHttp.post(url, centers_data);
    }

    mapViewService.uploadFile = function (proposal_id, societyfile){
      var url = url_base + proposal_id + '/import-society-data/';
      return machadaloHttp.post(url, societyfile);
    }

    //To get saved proposal data
    mapViewService.getShortlistedSuppliers = function(proposal_id){
    	// will receive proposal_id
        var url = url_base + "proposal/"+ proposal_id + "/shortlisted_suppliers/";
      	// var url = url_base + proposal_id;
    	return machadaloHttp.get(url);
    }

    mapViewService.updateSupplierStatus = function(proposal_id, data){
        var url = url_base + proposal_id + '/create-final-proposal/';
        return machadaloHttp.put(url, data);
    }

    //Start: code added for societydetails
    mapViewService.getSociety = function (id,supplierTypeCode) {
      console.log(id);
       var url = url_base_societyDetails + "supplier/" + id + "/image_details/?supplierTypeCode=" + supplierTypeCode;;
       return machadaloHttp.get(url);
    };

   //  mapViewService.get_inventory_summary = function(id){
   //   var url = url_base + "society/" + id + "/inventory_summary/";
   //   return machadaloHttp.get(url);
   //  };

    mapViewService.get_inventory_summary = function(id, supplierTypeCode){
      var url = url_base_societyDetails + "society/" + id + "/inventory_summary/?supplierTypeCode=" + supplierTypeCode;
      return machadaloHttp.get(url);
    };

    mapViewService.getSocietyList = function(data) {
      var url = url_base_societyDetails + "society/filterList/";
      return machadaloHttp.post(url, data);
    };

    mapViewService.getSocietyIds = function(){
       var url = url_base_societyDetails + "society/societyIds/";
       return machadaloHttp.get(url)
    }

    mapViewService.processParam = function(){
     if($stateParams.campaignId){
       $rootScope.campaignId = $stateParams.campaignId;
     }else {
       $rootScope.campaignId = null;
      }

      if($stateParams.societyId){
       $rootScope.societyId = $stateParams.societyId;
     }else {
       $rootScope.societyId = null;
     }
    };

    mapViewService.getShortlistedSocietyCount = function(campaign_id){
       var url = url_base_societyDetails + "website/campaign/" + campaign_id + "/society/count/";
       return machadaloHttp.get(url)
    }

    //for adding shortlisted societies
    mapViewService.addShortlistedSociety = function(campaign_id, society_id){
      var url = url_base_societyDetails + "website/campaign/society/shortlist/";
      var data = {campaign_id, society_id};
      return machadaloHttp.post(url, data);
    }
    //End: code added for societydetails

    return mapViewService;
}]);
