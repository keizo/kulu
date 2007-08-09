
 <?php if ($page == 0) { ?>
	 <div class="nodePreview<?php print ($sticky) ? " sticky" : ""; ?>">
	  <?php if ($title != ""): ?>
	  
	  <h2><div class="cornerR_yellow"></div>
	  
	  <a href="<?php print $node_url ?>" title="<?php print $title ?>">
	  <?php print $title ?></a>
	  </h2>
	  
	
	  <?php endif; ?>

	
	  <div class="content">
	  <div style="float:left"><?php print $taxonomy_images[0]; ?></div>
	  <?php print $content ?>
	  </div>
	  <?php if ($links): ?>

	  <div class="links"><?php print $links ?></div>
	  <?php endif; ?>
	</div>


  <?php } else { ?>
  
  
  <?php if ($title != ""): ?>
  <div id="title"><div class="cornerR_yellow"></div>
  <h1>
  <?php print $title ?>
  </h1>
<div id="info"><?php print $submitted .'<span class="taxonomy">'. ($submitted ? ' :: ' : '') . $terms .'</span>' ?></div>
  </div>

  <?php endif; ?>



  <div class="content"><div id="article_sidebar"></div>
  
  
  <?php print $content ?>
  <br />
    <p><em><?php print $submitted; ?> </em></p>
  </div>

<p><a href="/links">Back to Link Directory</a></p>
  <div class="links"></div>

  
<?php  
    //validation code
    $node->field_link[0]['value'] = check_url($node->field_link[0]['value']);
    $node->field_link[0]['value'] = ERegI('^[a-z0-9_]+://', $node->field_link[0]['value']) ? $node->field_link[0]['value'] : 'http://'.$node->field_link[0]['value'];
    //redirect code
    if (referer_uri()!="http://www.ocpaddler.com/node/add/link" && referer_uri()!="http://www.ocpaddler.com$node_url/edit") {
    header("HTTP/1.1 303 See Other");
    header("Location: " . $node->field_link[0]['value']);
    }
  ?>
  <?php } ?>

  
