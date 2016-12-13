 'use strict';
 angular.module('catalogueApp')
 .factory('opsDashBoardService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

    var url_base = 'v0/ui/website/';
    var opsDashBoard = {};

  	opsDashBoard.getProposalDetails = function(){
      var url = url_base + "proposal/invoice_proposals/";
  		return machadaloHttp.get(url);
  	}

    return opsDashBoard;
}]);
