var $titles = $('.title');
var $contents = $('.content');
var $container = $('.container');



$titles.on('click', function(){
	
	var $currentTitle = $(this);
	var $currentContent = $currentTitle.next();


	$contents.slideUp();
	if(!$currentContent.is(":visible"))
		{
			$currentContent.slideDown();
		}
});

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