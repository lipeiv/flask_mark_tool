var image = null;
var app = new Vue({
  el: '#app',
  data: {
    current_image: '/static/images/fruits.jpg',
    images: ['/static/images/1.jpg', '/static/images/2.jpg', '/static/images/3.jpg', '/static/images/4.jpg', '/static/images/5.jpg', '/static/images/6.jpg', '/static/images/7.jpg' ],
    object_categories: [{id: 1, name: "Apple"}, {id: 2, name: "Grape"}, {id: 3, name: "Watermelon"}, {id: 4, name: "Blueberry "}, {id: 5, name: "Banana"}, {id: 6, name: "Peach"}, {id: 7, name: "Melon"}],
    mark_elements: []
  }, 
  methods: {
    toggleElement: function(selectedElement) {
      var element_rect = selectedElement.svg_element.get(0);
      if(selectedElement.selected) {
        selectedElement.selected = false;
        element_rect.stroke({ width: 2, color: '#000'});
      } else {

        this.mark_elements.forEach(item =>{
          if(item != selectedElement) {
            item.selected = false;
            item.svg_element.get(0).stroke({ width: 2, color: '#000'});
          } else {
            selectedElement.selected = false;
            element_rect.stroke({ width: 2, color: '#FF9900'});
          }
        });

      }
      
    },

    removeElement: function(element, index) {
      element.svg_element.remove();
      this.$delete(this.mark_elements, index); 
    },

    selectImage: function(image_src) {
      console.log("Loading ", image_src);
      image.load(image_src);

      this.mark_elements.forEach(item =>{
        item.svg_element.remove();
      });

      this.mark_elements = [];
      this.current_image = image_src;
    }
  }
}); // new Vue

var drawa = SVG().addTo('#drawing').size(900, 500);
image = drawa.image('/static/images/fruits.jpg');

var drag_start = false;
var drag_draw_element = null;
var drag_start_point = {x:-1, y:-1};
var drag_end_point = {x:-1, y:-1};
var drag_new_rect = false;
var mouse_draged = false;

drawa.mousedown(function(e) {
  var point = {x: e.offsetX, y: e.offsetY};
  console.log("mousedown: point", point);
  drag_start = true;
  mouse_draged = false;
  drag_start_point = point;
});

drawa.mousemove(function(e) {
  console.log("mousemove");
  var current_point = {x: e.offsetX, y: e.offsetY};
  
  if(drag_start) {
    var points_5 = [[drag_start_point.x,drag_start_point.y], [current_point.x,drag_start_point.y], [current_point.x,current_point.y], [drag_start_point.x, current_point.y], [drag_start_point.x,drag_start_point.y]];
    if(drag_draw_element != null) {
      drag_draw_element.remove();
    }
    drag_draw_element = drawa.polyline(points_5).fill('none').stroke({ width: 2, color: '#000'});
  } else {

      app.mark_elements.forEach(item =>{
          var rect_box = item.svg_element.get(0);

      });

  }
});

drawa.mouseup(function(e) {
  var point = {x: e.offsetX, y: e.offsetY};
  var element_id = app.mark_elements.length;
  console.log("mouseup: point", point);

  var drag_distance_x = point.x - drag_start_point.x;
  var drag_distance_y = point.y - drag_start_point.y;
  if(drag_distance_x < 0) {
    drag_distance_x = -drag_distance_x;  
  }
  if(drag_distance_y < 0) {
    drag_distance_y = -drag_distance_y;  
  }
  var drag_offset_min = 7;
  if(drag_start && (drag_distance_x > drag_offset_min || drag_distance_y > drag_offset_min)) {
    mouse_draged = true;  
  } else {
    mouse_draged = false;
  }

  if(!mouse_draged) {
    drag_start = false;
    if(drag_draw_element != null) {
      drag_draw_element.remove();
      drag_draw_element = null;
    }
    return;
  }

  drag_start = false;

  var element_name = "Mark "+element_id;

  var box_group = drawa.group();

  drag_draw_element.mouseover(function(e){
    console.log("mouse hover on element.");
  });

  box_group.add(drag_draw_element);

  var text = drawa.text(element_name).attr({x:drag_start_point.x, y:drag_start_point.y });
  // text.font({anchor: 'middle', size: 30, family: 'Helvetica'});
  box_group.add(text);


  app.mark_elements.push({name: element_name, svg_element: box_group, selected: false});
  drag_draw_element = null;
});