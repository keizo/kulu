<div class="node<?php print ($sticky) ? " sticky" : ""; ?>">
 <?php if ($page == 0): ?>
  
  

	<table width="100%" border="0" cellpadding="5" cellspacing="0" bgcolor="#EBEBEB">
	  <tr> 
	    <td width="150" valign="top"><img src="<?php print $node->field_thumbnail_location[0]['value'] ?>"></td>
	    <td valign="top"> <h2><?php print $title ?></h2>
	      <?php print $node->field_video_description[0]['value'] ?>
<p>
 <a href="<?php print $node_url ?>" title="<?php print $title ?>">Watch Now</a> 
	      (<?php print $node->field_file_size_and_type[0]['value'] ?>) </p>
		  </td>
	  </tr>
	</table>


  <?php else: ?>


  <div class="info"><?php //print $submitted .'<span class="taxonomy">'. ($submitted ? ' :: ' : '') . $terms .'</span>' ?></div>
  <div class="content" align="center">
<br />
	        <h1><?php print $title ?></h1>
	        <table width="100%" border="0" cellpadding="0" cellspacing="0">
	          <tr>
	            <td align="center" valign="middle" bgcolor="#000000"> 
<?php if ($node->field_embedded_code[0]['value']  != ""): print $node->field_embedded_code[0]['value'] ; else: ?>				
	            <OBJECT classid='clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B' width="<?php print $node->field_video_width[0]['value']  ?>"
	        height="<?php print $node->field_video_height[0]['value']  + 14; ?>" codebase='http://www.apple.com/qtactivex/qtplugin.cab'>
	                <param name='src' value="<?php print $node->field_video_file_location[0]['value']  ?>">
	        <param name='autoplay' value="true">
	        <param name='controller' value="true">
	        <param name='loop' value="false">
	        <EMBED src="<?php print $node->field_video_file_location[0]['value']  ?>" width="<?php print $node->field_video_width[0]['value']  ?>" height="<?php print $node->field_video_height[0]['value']  + 14; ?>" autoplay="true" 
	        controller="true" loop="false" pluginspage='http://www.apple.com/quicktime/download/'>
	        </EMBED>
	        </OBJECT>
<?php endif; ?>
	            </td>
	          </tr>
	        </table>
			<p>
<?php print $node->field_video_description[0]['value'] ?>			
			</p>
<?php print $node->field_extra[0]['value'] ?>
<?php if ($node->field_embedded_code[0]['value'] == ""):	?>          
<p>If you have trouble viewing, make sure you have Quicktime. Freely available 
	          at <a href="http://www.quicktime.com">quicktime.com</a></p>
<?php endif; ?>
</div>
<div class="links"><strong><?php print $links ?></strong></div>
  <?php endif; ?>

</div>
  
