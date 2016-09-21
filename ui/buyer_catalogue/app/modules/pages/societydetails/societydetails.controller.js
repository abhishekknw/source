angular.module('machadaloPages')
.controller('SocietyCtrl',
    ['$scope', '$rootScope', '$window', '$location','societyDetailsService',
    function ($scope, $rootScope, $window, $location, societyDetailsService) {
     societyDetailsService.processParam();
     $scope.society = {};
     $scope.disable = false;
     $scope.residentCount = {};
     $scope.inventoryDetails = {};
     $scope.totalInventoryCount = {};
     societyDetailsService.getSociety($rootScope.societyId)
      .success(function (response) {
        $scope.society = response;
        $rootScope.societyname = response.society_name;
        $scope.residentCount = estimatedResidents(response.flat_count);
        $scope.flatcountflier = response.flat_count;
        console.log(response, "vidhi");
     });

     societyDetailsService.get_inventory_summary($rootScope.societyId)
     .success(function (response){
          $scope.inventoryDetails = response;
          $scope.totalInventoryCount = inventoryCount($scope.inventoryDetails);
          console.log($scope.inventoryDetails);
     });

     function estimatedResidents (flatcount){
       var residents = flatcount * 4;
       $scope.residentCount = {
          residents  : residents,
       };
       return $scope.residentCount;
     }
     function inventoryCount (inventoryDetails){
            var totalPoster = inventoryDetails.lift_count + inventoryDetails.nb_count ;
            $scope.totalInventoryCount = {
               totalPoster  : totalPoster,
            };
            return $scope.totalInventoryCount;
     }

    if($rootScope.campaignId){
        console.log("INside if");
        societyDetailsService.getShortlistedSocietyCount($rootScope.campaignId)
        .success(function(response,status){
            $scope.societies_count = response.count;
            console.log(response);

        }).error(function(response,status){
            console.log("error ",response.error);
            // console.log()
        });
    }

    // Done by me
    // $scope.index = 1;

    $scope.society_ids = {}
    societyDetailsService.getSocietyIds()
    .success(function(response,status){
        $scope.society_ids = response.society_ids;
        $scope.minlength = 0;
        $scope.maxlength = $scope.society_ids.length-1;
        for(var i=0;i<= $scope.maxlength; i++){
            if($rootScope.societyId == $scope.society_ids[i]){
                $scope.index = i;
                break;
            }
        }

        console.log($scope.society_ids)
    });


    $scope.nextSociety = function(){
        $scope.index = $scope.index + 1;
        if($scope.index <= $scope.maxlength){
            // getsocietyfunc($scope.model[$scope.index].supplier_id)
            var current_path = $location.path()
            var pos = current_path.lastIndexOf("/");
            var required_path = current_path.slice(0,pos+1) + $scope.society_ids[$scope.index] ;
            console.log("required_path  ",required_path);
            $location.path(required_path);
            // history.pushState({bar : "foo"}, "page 3", required_path);
            // setCurrentPage(required_path);
        }else{
            $scope.index = $scope.index - 1;
        }
        console.log("$index is : ",$scope.index)
    }

    $scope.previousSociety = function(){
       $scope.index = $scope.index - 1;
        if($scope.index >= $scope.minlength){
            var current_path = $location.path()
            var pos = current_path.lastIndexOf("/");
            var required_path = current_path.slice(0,pos+1) + $scope.society_ids[$scope.index] ;
            console.log("required_path  ",required_path);
            $location.path(required_path);
            // history.pushState({bar : "foo"}, "page 3", required_path);
            // setCurrentPage(required_path);
        }
        else{
           $scope.index = $scope.index + 1;
        }
        console.log("$index is : ",$scope.index)
    }

    $scope.societyByIndex = function(index){
        console.log("index received is : ", index);
        $scope.numberError = false;
        if(index <= $scope.maxlength && index >= $scope.minlength){
            $scope.index = index;
            var current_path = $location.path()
            var pos = current_path.lastIndexOf("/");
            var required_path = current_path.slice(0,pos+1) + $scope.society_ids[$scope.index] ;
            $location.path(required_path);
        }
        else{
            $scope.numberError = true;
             // $scope.startFade = true;
             //  $timeout(function(){
             //    $scope.numberError = true;
             //  }, 2000);
        }
        $scope.societyIndex = undefined;
        console.log("$index is : ",$scope.index)
    }

     $scope.societyList = function() {
       $location.path("manageCampaign/shortlisted/" + $rootScope.campaignId + "/societies");
     };

     //Start:For adding shortlisted society
     if($rootScope.campaignId){
       $scope.shortlistThis = function(id) {
       societyDetailsService.addShortlistedSociety($rootScope.campaignId, id)
        .success(function (response){
            // $scope.model = response;
              console.log("You received response as");
              console.log(response);
              // $location.path("manageCampaign/shortlisted/" + $rootScope.campaignId + "/societies");
              $scope.disable = true;
              $scope.societies_count = response.count;

              // var temp = "#alert_placeholder" + index;
              var temp = "#alert_placeholder";
            var style1 = 'style="position:absolute;z-index:1000;margin-left:-321px;margin-top:-100px;background-color:gold;font-size:18px;"'
            $(temp).html('<div ' + style1 + 'class="alert alert-warning alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>'+response.message +'</span></div>')
            setTimeout(function() {
                $("div.alert").remove();
            }, 3000);
            // $("#alert_placeholder").html('<div> shortlisted</div>')
       });
     }}//End: For adding shortlisted society
   }]);//Controller function ends here
