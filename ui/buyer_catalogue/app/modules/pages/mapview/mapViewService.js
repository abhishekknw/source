 'use strict';
 angular.module('catalogueApp')
 .factory('mapViewService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

    var url_base = 'v0/ui/website/';
    var mapViewService = {};

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
        var url = url_base + proposal_id + '/export-spaces-data/';
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

    return mapViewService;
}]);
