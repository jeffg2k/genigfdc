/* App Module */
var geniframework = angular.module('geniframework', []);

geniframework.config(['$routeProvider', function($routeProvider){
	$routeProvider.when('/home', {
		templateUrl : '../../static/partials/home.html',
		controller : HomeController
	});
    $routeProvider.when('/unique', {
		templateUrl : '../../static/partials/unique.html',
		controller : UniqueController
	});
    $routeProvider.when('/top50', {
		templateUrl : '../../static/partials/top.html',
		controller : Top50Controller
	});
	$routeProvider.otherwise({
    	redirectTo : '/unique'
	});
}]);

function HomeController($scope,$rootScope, $http){
    var httpPromise = $http;
    var profileAPI = '/getProfile';
    $scope.loading = true;
    callServerGETAPI(httpPromise, profileAPI, procesSearch);

    $scope.recentProfiles = [];

    function procesSearch(responseData){
        $scope.loading = false;
        $('.loadingMask').hide();
        $scope.profileData = responseData;
        $scope.profileId = $scope.profileData.id;
        $scope.profileName = $scope.profileData.name;
    }

    $scope.getProfile = function(id, name){
        var profileAPI = 'js/json/' + id+'.js';
        $scope.loading = true;
        $('.loadingMask').show();
        callServerGETAPI(httpPromise, profileAPI, procesSearch);
        if($scope.recentProfiles.length === 0){
            var profileObj = {"id" : $scope.profileId, "name" : $scope.profileName}
            $scope.recentProfiles.push(profileObj);
        }else{
          var count = 0;
            var profileObj = {"id" : $scope.profileId, "name" : $scope.profileName};
            $.each($scope.recentProfiles, function(index, value) {
                //console.log(JSON.stringify($scope.recentProfiles));
                //console.log(value.id + "------" + id);
              if(value.id === $scope.profileId){
				 count = count + 1;
			  }
		   });
            if(count === 0){
                $scope.recentProfiles.push(profileObj);
            }
        }
    }
}

var UniqueController = function($scope,$rootScope, $http){
    var httpPromise = $http;
    /*$scope.loading = true;
    $('.loadingMask').show();
    var onloadProfileData = 'js/json/onloadProfileCountJSON.js';
    var me = this;
    callServerGETAPI(httpPromise, onloadProfileData, loadProfileData);

    function loadProfileData(responseData){
        $scope.loading = false;
        $('.loadingMask').hide();
      $scope.isProfileExists = responseData.profileId;
      if(angular.isUndefined($scope.isProfileExists)){
            $scope.showUserProfile = true;
            $scope.myProfileData = responseData;
            $('#uniqueProfilesTab a[href="#profile"]').tab('show');
      }else{
            $scope.showUserProfile = false;
            $scope.otherProfileData = responseData;
            $('#uniqueProfilesTab a[href="#otherProfile"]').tab('show');
      }
    }*/
    $('#uniqueProfilesTab a[href="#profile"]').tab('show');
    $scope.showTableDataMyProfile = false;
    $scope.showTableDataOtherProfile = false;
    $scope.submitMyProfile = function(formId){
        var getFormData = $(formId).serialize();
        $rootScope.formId = formId;
        var submiProfileAPI = '/getUniqueCount?'+getFormData;
        if($rootScope.formId === '#myProfileForm'){
           if($scope.myProfileForm.stepValue < 4){
                if($scope.myProfileForm.stepValue !== ''){
                    $scope.loading = true;
                    $('.loadingMask').show();
                    callServerGETAPI(httpPromise, submiProfileAPI, showTableData);
                }
           }else{
                if(($scope.myProfileForm.stepValue !== '') && ($scope.myProfileForm.emailField !== '')
                   && ($scope.myProfileForm.email.$valid)){
                    $scope.loading = true;
                    $('.loadingMask').show();
                    callServerGETAPI(httpPromise, submiProfileAPI, showTableData);
                }
           }
        }else{
            if($scope.otherProfileForm.stepValue < 4){
                if($scope.otherProfileForm.stepValue !== ''){
                    $scope.loading = true;
                    $('.loadingMask').show();
                    callServerGETAPI(httpPromise, submiProfileAPI, showTableData);
                }
            }else{
                if(($scope.otherProfileForm.stepValue !== '') && ($scope.otherProfileForm.emailField !== '')
                   && ($scope.otherProfileForm.email.$valid)){
                    $scope.loading = true;
                    $('.loadingMask').show();
                    callServerGETAPI(httpPromise, submiProfileAPI, showTableData);
                }
            }
        }
    }

    function showTableData(responseData){
        $scope.loading = false;
        $('.loadingMask').hide();
        if($rootScope.formId === '#otherProfileForm'){
            $scope.otherProfileData = responseData;
            if(! angular.isUndefined($scope.otherProfileData.backgroundMessage)){
                $scope.otherProfileFormSuccessMsg = true;
                $('#otherProfileFormSuccessMsg').html($scope.otherProfileData.backgroundMessage);
                setTimeout(function(){
                    $scope.otherProfileFormSuccessMsg = false;
                    $('#otherProfileFormSuccessMsg').fadeOut('slow');
                }, 1500);
            };
            $scope.showTableDataOtherProfile = true;
            $scope.otherProfileForm.stepValue = null;
            $scope.otherProfileForm.emailField = null;
        }else{
            $scope.myProfileData = responseData;
            console.log(!angular.isUndefined($scope.myProfileData.backgroundMessage));
            if(!angular.isUndefined($scope.myProfileData.backgroundMessage)){
                $scope.myProfileFormSuccessMsg = true;
                $('#myProfileFormSuccessMsg').html($scope.myProfileData.backgroundMessage);
                setTimeout(function(){
                    $scope.myProfileFormSuccessMsg = false;
                    $('#myProfileFormSuccessMsg').fadeOut('slow');
                }, 1500);
            };
            $scope.showTableDataMyProfile = true;
            $scope.myProfileForm.stepValue = null;
            $scope.myProfileForm.emailField = null;
        }
    }

};

var Top50Controller = function($scope,$rootScope, $http){
    var httpPromise = $http;
    $scope.loading = true;
    $('.loadingMask').show();
    var top50ProfileData = '/top';
    callServerGETAPI(httpPromise, top50ProfileData, showTop50Profiles);

    function showTop50Profiles(responseData){
        $scope.loading = false;
        $('.loadingMask').hide();
        $scope.top50Profiles = responseData.top50;
    }
};
function callServerGETAPI(httpPromise, apiName, reponseHandler){
	httpPromise.get(apiName).success(reponseHandler);
}
