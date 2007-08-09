<?php drupal_set_html_head('<style type="text/css" media="all">@import "/' . path_to_theme() . '/node-page.css";</style>');  ?> 

 <?php if ($page == 0) { ?>
	 <div class="<?php print ($sticky) ? " stickypage" : "nodePreview"; ?>">
	  <?php if ($title != "" && $sticky != 1): ?>
	  
	  <h2>
	  <a href="<?php print $node_url ?>" title="<?php print $title ?>">
	  <?php print $title ?></a>
	  </h2>
	  
	
	  <?php endif; ?>

	
	  <div class="content">
	  <?php print $content ?>
	  </div>
	  
	  <?php if ($links && $sticky != 1): ?>
	<div class="links">
	  <?php print $links ?>
	</div>
	  <?php endif; ?>
	  
	</div>

  <?php } else { ?>
  <?php if ($title != ""): ?>
  <div id="title">
  <h1>
  <?php print $title ?>
  </h1>
   </div>

  <?php endif; ?>



  <div class="content"><div id="article_sidebar"></div>
  <?php print $content ?>
  </div>
  <?php if ($links): ?>

  <div class="links"><?php print $links ?></div>
  <?php endif; ?>
  <?php } ?>

  
