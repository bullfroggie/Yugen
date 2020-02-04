(function(angular) {
    let app = angular.module("app");

    app.controller("AccommodationCtrl", [
        "$http",
        "$scope",
        function($http, $scope) {
            let that = this;

            this.accommodations = [];

            this.searched = null;
            this.stars = 0;

            $scope.isReadonly = true;
            $scope.unavailableCounter = 0;

            this.getAccommodations = function() {
                $http.get("api/accommodation/city/" + that.searched).then(
                    function(response) {
                        console.log(response);
                        that.accommodations = response.data;
                        that.stars = 0;
                        if (that.accommodations.length == 0) {
                            console.log("No accommodation for " + that.searched + " found.");
                            $scope.unavailableCounter = 0;
                        }
                        for (let accommodation of that.accommodations) {
                            if (accommodation.available == 0) {
                                $scope.unavailableCounter++;
                            }
                        }

                        that.getImages();
                    },
                    function(reason) {
                        console.log(reason);
                        if (reason.status == 404) {
                            that.accommodations = [];
                        }
                    }
                );
            };

            this.filterByStars = function() {
                $scope.unavailableCounter = 0;
                $http.get("api/accommodation/filter/" + that.searched + "/" + that.stars).then(
                    function(response) {
                        console.log(response);
                        that.accommodations = response.data;
                        $scope.unavailableCounter = 0;
                        if (that.accommodations.length == 0) {
                            console.log(
                                "No accommodation in " +
                                    that.searched +
                                    " with " +
                                    that.stars +
                                    " stars found."
                            );
                        }
                        for (let accommodation of that.accommodations) {
                            if (accommodation.available == 0) {
                                $scope.unavailableCounter++;
                            }
                        }
                        that.getImages();
                    },
                    function(reason) {
                        console.log(reason);
                        if (reason.status == 404) {
                            that.accommodations = [];
                        }
                    }
                );
            };

            this.getImages = function() {
                $http.get("api/accommodation/images").then(
                    function(response) {
                        console.log(response);
                        this.images = response.data;

                        for (let accommodation of that.accommodations) {
                            accommodation.images = [];
                            for (let image of images) {
                                if (accommodation.name == image.name) {
                                    accommodation.images.push(image.path);
                                }
                            }
                        }
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };
        }
    ]);
})(angular);
