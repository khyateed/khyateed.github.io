var $title = $('.title');
var $contents = $('.content');
var $container = $('.container');
var $container_stuff = $('.container_stuff');


// changes title background color on hover
$title.on('mouseover', function(){
	var $currentTitle = $(this);

	$currentTitle.css("background", "#333");
	$currentTitle.css("color", "white");
});


$title.on('mouseout', function(){
	var $currentTitle = $(this);
	$currentTitle.css("background", "#e2e2e2");
	$currentTitle.css("color", "#333");
});


// expands titles to show containers
$contents.slideUp();
$title.on('click', function(){
	
	var $currentTitle = $(this);
	var $currentTitleContent = $currentTitle.next();

	$contents.slideUp();
	$title.css("background", "#e2e2e2");
	$title.css("color", "#333");
	$container_stuff.slideUp()
	if(!$currentTitleContent.is(":visible"))
		{
			$currentTitleContent.slideDown();
			$currentTitle.css("background", "#333");
			$currentTitle.css("color", "white");
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
	$currentImg.css("-webkit-filter", "brightness(100%)");
	$currentCaption.hide();
});

// expands more contents of each container when clicked
$container.on('click', function(){
	var $currentContainer = $(this);
	var $currentContainerStuff = $currentContainer.next().next().next();

	$container_stuff.slideUp();
	if(!$currentContainerStuff.is(":visible"))
		{	
			$currentContainerStuff.slideDown();
		}
});