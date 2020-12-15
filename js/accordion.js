var $category = $('.category');
var $contents = $('.content');
var $container = $('.container');
var $container_stuff = $('.container_stuff');
var $container_img = $container.find('img');
var $caption = $('.caption');


// changes category background color on hover
$category.on('mouseover', function(){
	var $currentCategory = $(this);

	$currentCategory.css("background", "#333");
	$currentCategory.css("color", "white");
});


$category.on('mouseout', function(){
	var $currentCategory = $(this);
	$currentCategory.css("background", "#e2e2e2");
	$currentCategory.css("color", "#333");
});


// expands Categories to show containers
// $contents.slideUp();
$category.on('click', function(){
	
	var $currentCategory = $(this);
	var $currentCategoryContent = $currentCategory.next();

	$contents.slideUp();
	$category.css("background", "#e2e2e2");
	$category.css("color", "#333");
	$container_img.css("-webkit-filter", "brightness(100%)");
	$caption.hide();
	$container_stuff.slideUp();
	if(!$currentCategoryContent.is(":visible"))
		{
			$currentCategoryContent.slideDown();
			$currentCategory.css("background", "#333");
			$currentCategory.css("color", "white");
		}
});

// dims each container background + shows caption
$container.on('mouseover', function(){
	var $currentContainer = $(this);
	var $currentCaption = $currentContainer.find('div');
	var $currentImg = $currentContainer.find('img');
	$currentImg.css("-webkit-filter", "brightness(50%)");
	$currentCaption.show();
});


$container.on('mouseout', function(){
	var $currentContainer = $(this);
	var $currentCaption = $currentContainer.find('div')
	var $currentImg = $currentContainer.find('img');
	var $currentContainerStuff = $currentContainer.next().next().next();

	if(!$currentContainerStuff.is(":visible"))
	{	
		$currentImg.css("-webkit-filter", "brightness(100%)");
		$currentCaption.hide();

		}

});

// expands more contents of each container when clicked
$container.on('click', function(){
	var $currentContainer = $(this);
	var $currentContainerStuff = $currentContainer.next().next().next();
	var $currentCaption = $currentContainer.find('div');
	var $currentImg = $currentContainer.find('img');


		$container_img.css("-webkit-filter", "brightness(100%)");
		$caption.hide();
		$container_stuff.slideUp();

	if(!$currentContainerStuff.is(":visible"))
		{	
			$currentContainerStuff.slideDown();
			$currentImg.css("-webkit-filter", "brightness(50%)");
			$currentCaption.show();
		}

});