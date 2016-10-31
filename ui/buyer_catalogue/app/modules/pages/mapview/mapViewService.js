 'use strict';
 angular.module('catalogueApp')
 .factory('mapViewService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

    var url_base = 'v0/ui/website/';
    var mapViewService = {};

    mapViewService.getSpaces = function(proposal_id){
        // done
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

    mapViewService.createFinalProposal = function(proposal_id, centers_data){
        var url = url_base + proposal_id + '/createFinalProposal/';
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
    return mapViewService;
}]);
