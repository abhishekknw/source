'use strict';

/**
 * @ngdoc function
 * @name societyCatalogApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the societyCatalogApp
 */
angular.module('societyCatalogApp')
  .controller('societyDetailsCtrl', function ($scope, $http, societyDetailsService) {

    
  	getSociety();

    $scope.society = {"supplierId":1,
    "societyName":"Nahar Amrit Shakti",
    "societyAddress1":"Park Street","societyAddress2":"Powai","societyZip":"1","societyCity":"Kolkata",
    "societyState":"1","societyLongitude":"72.9100","societyLattitude":"19.1200",
    "societyLocationType":"1","societyTypeQuality":"1","societyTypeQuantity":"1",
    "flatCount":1,"residentCount":1,"carsCount":1,
    "luxuryCarsCount":1,"machadaloIndex":"4","averageRent":"1",
    "noticeBoardAvailable":true,"carDisplayAvailable":true,"eventsCount":1,
    "swimmingPoolAvailability":true,"mailBoxAvailable":true,"doorToDoorAllowed":true,
    "streetFurnitureAvailable":true}

   
  

    function getSociety() {
      societyDetailsService.getSocietyData()
        .then(function (response) {
          $scope.ss = response.data;
          console.log($scope.ss)

        })
        .catch(function (error) {
          $scope.status = 'Unable to load society data: ' + error.message;
        });
    }



  });

