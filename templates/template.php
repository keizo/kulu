<?php
/**
* Theme the forums to look like phpBB
*/
function _phptemplate_variables($hook, $vars) {
  static $is_forum;
  $variables = array();
  if (!isset($is_forum)) {
    if (arg(0) == 'node' && is_numeric(arg(1)) && arg(2) == '') {
      $nid = arg(1);
    }
    if (arg(0) == 'comment' && arg(1) == 'reply' && is_numeric(arg(2))) {
      $nid = arg(2);
    }
    if ($nid) {
      $node = node_load(array('nid' => $nid));
    }
    $is_forum = ($node && $node->type == 'forum');
    _is_forum($is_forum);
  }
  if ($is_forum) {
    switch ($hook) {
      case 'comment' :
        $variables['template_file'] = 'node-forum';
        $variables['row_class'] = _row_class();
        $variables['name'] = $vars['author'];
        $variables['userid'] = $vars['comment']->uid;
        $joined = module_invoke('flatforum', 'get_created', $vars['comment']->uid);
        $variables['joined'] = $joined ? format_date($joined, 'custom', 'Y-m-d') : '';
        $posts = module_invoke('flatforum', 'get', $vars['comment']->uid);
        $variables['posts'] = $posts ? $posts : 0;
        $variables['submitted'] = format_date($vars['comment']->timestamp);
        $subject = $vars['comment']->subject;
        $variables['title'] = empty($subject) ? '&nbsp' : $subject;
        $variables['content'] = $vars['comment']->comment;
        $variables['links'] = empty($vars['links']) ? '&nbsp' : $vars['links'];
        break;
      case 'node' :
        $variables['row_class'] = _row_class();
        $variables['userid']=$vars['node']->uid;
        $joined = module_invoke('flatforum', 'get_created', $vars['node']->uid);
        $variables['joined'] = $joined ? format_date($joined, 'custom', 'Y-m-d') : '';
        $posts = module_invoke('flatforum', 'get', $vars['node']->uid);
        $variables['posts'] = $posts ? $posts : 0;
        $variables['title'] = empty($vars['title']) ? '&nbsp' : $vars['title'];
        $variables['content'] = $vars['node']->body;
        $variables['links'] = empty($vars['links']) ? '&nbsp' : $vars['links'];
        break;
    }
  }
  if ($hook == 'node') {
    if (module_exists("taxonomy_image")) {
       foreach (taxonomy_node_get_terms($vars['node']->nid) as $term) {
        $variables['taxonomy_images'][] = taxonomy_image_display($term->tid);
       }
    }
    if (module_exists("taxonomy_text")) {
       foreach (taxonomy_node_get_terms($vars['node']->nid) as $term) {
        $variables['taxonomy_text'][] = taxonomy_text_display($term->tid);
       }
    }
  }  

  return $variables;
}
function _row_class() {
  static $forum_row = TRUE;
  $forum_row = !$forum_row;
  return $forum_row ? 'odd' : 'even';
}
function _is_forum($arg = NULL) {
  static $is_forum = FALSE;
  if ($arg) {
    $is_forum = $arg;
  }
  return $is_forum;
}

/*
function phptemplate_comment_form($edit, $title) {
$form = (is_file(path_to_theme(). 'comment_form.tpl.php') ?
_phptemplate_callback('comment_form', array('edit' => $edit, 'title' => $title)) :
theme_comment_form($edit, $title));
return _is_forum() ? '<tr><td colspan="2">'. $form  .'</td></tr>' : $form;
}*/
function phptemplate_pager($tags = array(), $limit = 10, $element = 0, $attributes = array()) {
$pager = (is_file(path_to_theme(). 'pager.tpl.php') ?
_phptemplate_callback('comment_form', array('tags' => $tags, 'limit' => $limit, 'element' => $element, 'attributes' => $attributes)) :
theme_pager($tags, $limit, $element, $attributes));
return _is_forum() ? '<tr><td colspan="2">'. $pager .'</td></tr>' : $pager;
}

/**
* This snippet works with Drupal 4.7 
* and will NOT work with Drupal 4.5 or Drupal 4.6
*/

function phptemplate_profile_listing($user, $fields = array()) {
/**
* This snippet catches the default user list pages layout
* and looks for a profile_listing.tpl.php file in the same folder
* which has the new layout.
*/
return _phptemplate_callback('profile-profile', array('user' => $user, 'fields' => $fields));
  }

/**
* Catch the theme_profile_profile function, and redirect through the template api
*/
function phptemplate_user_profile($user, $fields = array()) {
  // Pass to phptemplate, including translating the parameters to an associative array. The element names are the names that the variables
  // will be assigned within your template.
  /* potential need for other code to extract field info */
return _phptemplate_callback('user_profile', array('profile' => $user, 'fields' => $fields));
  }
  
  
/*
// if you want a totally different group home page, you may redefine this function in your theme
// if you just want to change the presentation of a group home page section, redefine theme_og_list_generic()
function phptemplate_og_view(&$node, $teaser = FALSE, $page = FALSE) {
  if ($teaser || !$page) {
    $node->teaser = $node->og_description;
    $node = node_prepare($node, $teaser);
  }
  else {
  	$node = node_prepare($node, $teaser);
    $bc = array(l(t('Home'), ''), l(t('groups'), 'og'));
    drupal_set_breadcrumb($bc);
    $output =''; $output_page = '';
    $mode = 'all';

    if (!$types[] = $_GET['ntype']) {
      $types = node_list();
      $mode = 'brief';
    }
    foreach ($types as $type) {
      // image is filtered out here because we expect images to be added from within albums
      $exempt = array_merge(array('og', 'image'), variable_get('og_omitted', array()));
      if (!in_array($type, $exempt)) {
        if ($table = og_list_og($node->nid, $type, $mode)) {
          $output .= $table;
        }        
      }
    }

    if (!$output) {
      drupal_set_message(t('No posts in this group.'));
    }
    $url = url("og/feed/$node->nid");
    $icon = theme('xml_icon', $url);
    drupal_set_html_head("<link rel=\"alternate\" href=\"$url\" title=\"$node->title RSS feed\" type=\"application/rss+xml\" />");
    $node->body .= $output. $icon;
  }
  return $node;
}
// you may theme this function, or even theme each node type listing separately
function phptemplate_page_list_og($gid, $mode) {
  static $i;
	$type = 'page';
			$header = array(t('Title'));
			$sql = og_get_home_nodes_sql($type);
			$num = $mode == 'brief' ? variable_get('og_max_posts', 10) : 50;
			$i++; // multiple pagers on a page need a unique integer
			$result = pager_query(db_rewrite_sql($sql), $num, $i, NULL, $gid);
			while ($row = db_fetch_object($result)) {
				$rows[] = array(l($row->title, "node/$row->nid"));
			}
			if ($pager = theme('pager', NULL, $num, $i, array('ntype' => $type))) {
				$rows[] = array(array('data' => $pager, 'colspan' => '4'));
			}		
  return $rows ? form_group(node_invoke($type, 'node_name'), theme('table', $header, $rows)) : NULL;
}
*/

?>
