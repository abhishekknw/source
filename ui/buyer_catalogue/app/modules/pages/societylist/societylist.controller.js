angular.module('machadaloPages')
.controller('SocietyListCtrl',
    ['$scope', '$rootScope', '$window', '$location', '$http','societyListService', 'pagesService',
    function ($scope, $rootScope, $window, $location, $http, societyListService, pagesService) {
      societyListService.processParam();
    //Start: For displaying filter values
      $scope.otherFilters = [];
      $scope.locationValueModel = [];
      $scope.locationValue = [];
      $scope.subLocationValueModel = [];
      $scope.subLocationValue = [];
      $scope.typeValue = [];
      $scope.typeValuemodel = [];
      $scope.showSubAreas = false;
      $scope.locationValueSettings = {
        scrollableHeight: '100px',
        scrollable: true,
        externalIdProp: '',
        dynamicTitle: true,
      };
      $scope.locationcustomTexts = {
        buttonDefaultText: 'Select Area',
        checkAll: 'Select All',
        uncheckAll: 'Select None',
        dynamicButtonTextSuffix: 'Value'
      };

      $scope.locationSubAreaCustomTexts = {
        buttonDefaultText : 'Select SubArea',
        checkAll : 'Select All',
        uncheckAll : 'Select None',
        dynamicButtonTextSuffix: 'Value',
      };

      $scope.locationSubAreaSettings = {
        scrollableHeight: '100px',
        scrollable: true,
        externalIdProp: '',
        dynamicTitle: true,
        displayProp : 'subarea_name',
      };
     

      $scope.typeValue = [
       {id: 1, label: "Ultra High"},
       {id: 2, label: "High"},
       {id: 3, label: "Medium High"},
       {id: 4, label: "Standard"}
      ];
      $scope.typecustomTexts = {
        buttonDefaultText: 'Select Society Type',
        checkAll: 'Select All',
        uncheckAll: 'Select None'
      };
      $scope.checkboxes = [];
      var flattype = [
        {"name":"Small", checked: false},
        {"name":"Medium", checked: false},
        {"name":"Large", checked: false},
        {"name":"Very Large", checked: false}
    ];
    $scope.checkboxes = flattype;
    $scope.types = [];
    var inventorytype = [
      {"inventoryname": "Poster Campaign", checked: false},
      {"inventoryname": "Standee Campaign", checked: false},
      {"inventoryname": "Stall Campaign", checked: false},
      {"inventoryname": "Car Display Campaign", checked: false},
      {"inventoryname": "Flier Campaign", checked: false}
    ];
    $scope.types = inventorytype;

      societyListService.listFilterValues()
      .success(function (response){
        $scope.locationValue = response;
        console.log("List Filter Values");
        console.log($scope.locationValue);
        console.log("\n\n\n")
      })

      

      $scope.getSubAreas = function(){
        $scope.subLocationValue = [];
        $scope.showSubAreas = true;
        console.log($scope.locationValueModel);
        societyListService.getSubAreas($scope.locationValueModel)
        .success(function(response, status){
            $scope.subLocationValue = response;
            console.log("Sub Location Values");
            console.log($scope.subLocationValue)
        });
        $scope.showSubAreas = true;
      };


      $scope.model = {};
        var sObj = '';
       societyListService.getSocietyList({},sObj)
          .success(function (response) {
             $scope.model = response;
             console.log("$scope.model Values");
             console.log($scope.model);

      });

    
     $scope.filterResult = {};
      $scope.filterSocieties = function(typeValuemodel, locationValueModel, subLocationValueModel, checkboxes, types) {
        var mySource1 = {locationValueModel};
        var mySource2 = {typeValuemodel};
        var mySource3 = {checkboxes};
        var mySource4 = {types}
        var mySource5 = {subLocationValueModel}
        var myDest = {}
        angular.extend(myDest, mySource1, mySource2, mySource3, mySource4, mySource5)
        console.log(myDest);
        societyListService.getSocietyList(myDest,"")
         .success(function (response){
           $scope.model = response;
           console.log("After filtering ");
           console.log(response);
        });
      }
      //End: For displaying filter values

    $scope.clearFilter = function (){
      $scope.locationValueModel = [];
      $scope.typeValuemodel = [];
      var flattype = [
        {"name":"Small", checked: false},
        {"name":"Medium", checked: false},
        {"name":"Large", checked: false},
        {"name":"Very Large", checked: false}
      ];
      $scope.checkboxes = flattype;
      var inventorytype = [
        {"inventoryname": "Poster Campaign", checked: false},
        {"inventoryname": "Standee Caimpaign", checked: false},
        {"inventoryname": "Stall Campaign", checked: false},
        {"inventoryname": "Car Display Campaign", checked: false},
        {"inventoryname": "Flier Campaign", checked: false}
      ];
      $scope.types = inventorytype;
      societyListService.getSocietyList({},"")
         .success(function (response) {
            $scope.model = response;
            console.log($scope.model);

     });
    }

   //Start:For adding shortlisted society
   $scope.disable = false;
   if($rootScope.campaignId){
     $scope.shortlistThis = function(id,index) {
     $scope.model[index].disable = true;
     societyListService.addShortlistedSociety($rootScope.campaignId, id)
      .success(function (response){
           
          var temp = "#alert_placeholder" + index;
          var style1 = 'style="position:absolute;z-index:1000;margin-left:-321px;margin-top:-100px;background-color:gold;font-size:18px;"'
          $(temp).html('<div ' + style1 + 'class="alert alert-warning alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>'+response.message +'</span></div>')
          setTimeout(function() {
              $("div.alert").remove();
          }, 3000);
          console.log(response.message);
     });
   }}//End: For adding shortlisted society

   //Start: To navigate to catalogue page
   if($rootScope.campaignId){
   $scope.catalogue = function(id){
     // alert(id);
     $location.path('campaign/' + $rootScope.campaignId +'/societyDetails/' + id);
   }}//End: To navigate to catalogue page

  

  //Start: Sort Functionality
      $scope.predicate = 'society_name';
      $scope.reverse = 'asc';

      $scope.order = function(predicate) {

        var society_ids = []
        for(var i=0;i<$scope.model.length;i++)
            society_ids.push($scope.model[i].supplier_id);

          if($scope.reverse === 'asc'){
              $scope.reverse = 'desc';
          }
          else{
              $scope.reverse = 'asc';
          }
        societyListService.getSortedSocieties($scope.reverse,society_ids)
        .success(function(response,status){
              $scope.model = response;
              console.log('got sorted societies')
        }).error(function(response,status){
              // $scope.errorMsg = response.message;
              console.log('unable to get sorted societies');
        });

    }
  //End: Sort Functionality


    // var i = 0;
    // $scope.tempArray = [];
    // $scope.onItemSelect = function(property) {
    //     i++;
    //     if ($scope.tempArray === $scope.locationValueModel){
    //         console.log("Both array are equal")
    //     }else{
    //       if(i % 2 == 0){
    //         console.log("Unequal Array", i);
    //             angular.copy($scope.locationValueModel, $scope.tempArray);
    //             console.log($scope.locationValueModel);
    //             console.log($scope.tempArray);
    //       }
    //     }
    //     // console.log($scope.locationValueModel);
     
    // }

  $scope.societyList = function() {
    $location.path("manageCampaign/shortlisted/" +$rootScope.campaignId + "/societies");
  };
  /*//pagination starts here
  $scope.totalItems = 64;
  $scope.currentPage = 4;

  $scope.setPage = function (pageNo) {
    $scope.currentPage = pageNo;
  };

  $scope.pageChanged = function() {
   alert('gvg');
  };
  $scope.maxSize = 5;
  $scope.bigTotalItems = 175;
  $scope.bigCurrentPage = 1;
    //pagination ends here
*/
}]);
