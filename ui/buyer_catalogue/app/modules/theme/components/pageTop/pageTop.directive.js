/**
 * @author v.lugovksy
 * created on 16.12.2015
 */
(function () {
  'use strict';

  angular.module('machadaloCommon')
      .directive('pageTop', pageTop);

  /** @ngInject */
  function pageTop() {
    return {
      restrict: 'E',
      templateUrl: 'modules/theme/components/pageTop/pageTop.html',
      link: function($scope, element, attrs) {
                // $scope.perm = permissions.navBar;
                // Do some stuff
                $scope.closeModal = function(){
                  $('#menuModal').modal('hide');
                   $('body').removeClass('modal-open');
                   $('.modal-backdrop').remove();
                }
          }

    };
  }

})();
