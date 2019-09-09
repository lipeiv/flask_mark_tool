window.addEventListener("load", function(event) {
  var vue_app = new Vue({
  el: '#app',
  data: {
    svg_draw: null,
    svg_bg_image: null,
    images: [
              {thumb_url:'/img/0', url:'/img/0', marks: []},
              {thumb_url:'/img/1', url:'/img/1', marks: []},
              {thumb_url:'/img/2', url:'/img/2', marks: []},
              {thumb_url:'/img/3', url:'/img/3', marks: []},
              {thumb_url:'/img/4', url:'/img/4', marks: []},
              {thumb_url:'/img/5', url:'/img/5', marks: []},
              {thumb_url:'/img/6', url:'/img/6', marks: []},
              {thumb_url:'/img/7', url:'/img/7', marks: []},
              {thumb_url:'/img/8', url:'/img/8', marks: []},
              {thumb_url:'/img/9', url:'/img/9', marks: []}
            ],
    mark_categories: [
                        {id: 1, name: "Apple"}, 
                        {id: 2, name: "Grape"}, 
                        {id: 3, name: "Watermelon"}, 
                        {id: 4, name: "Blueberry "}, 
                        {id: 5, name: "Banana"}, 
                        {id: 6, name: "Peach"}, 
                        {id: 7, name: "Melon"},
                        {id: 8, name: "Strawberry"}
                      ],
    current_image: null
  },
  mounted: function () {
    var _this = this;
    var drag_start = false;
    var drag_draw_element = null;
    var drag_start_point = {x:-1, y:-1};
    var drag_end_point = {x:-1, y:-1};
    var drag_new_rect = false;
    var mouse_draged = false;
    this.svg_draw = SVG().addTo('#drawing').size(900, 500);
    this.svg_bg_image = this.svg_draw.image("/static/images/1.jpg");

    this.svg_draw.mousedown(function(e) {
      var point = {x: e.offsetX, y: e.offsetY};
      console.log("mousedown: point", point);
      drag_start = true;
      mouse_draged = false;
      drag_start_point = point;
    });

    this.svg_draw.mousemove(function(e) {
      console.log("mousemove");
      var current_point = {x: e.offsetX, y: e.offsetY};
      
      if(drag_start) {
        var points_5 = [[drag_start_point.x,drag_start_point.y], [current_point.x,drag_start_point.y], [current_point.x,current_point.y], [drag_start_point.x, current_point.y], [drag_start_point.x,drag_start_point.y]];
        if(drag_draw_element != null) {
          drag_draw_element.remove();
        }
        drag_draw_element = _this.svg_draw.polyline(points_5).fill('none').stroke({ width: 2, color: '#000'});
      } else {

          /*
          vue_app.mark_elements.forEach(item =>{
              var rect_box = item.svg_element.get(0);
          });
          */

      }
    });

    this.svg_draw.mouseup(function(e) {
      var point = {x: e.offsetX, y: e.offsetY};
      var element_id = _this.current_image.marks.length;
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

      var element_name = _this.mark_categories[0].name;

      var box_group = _this.svg_draw.group();

      drag_draw_element.mouseover(function(e){
        console.log("mouse hover on element.");
      });

      box_group.add(drag_draw_element);

      var text = _this.svg_draw.text(element_name).attr({x:drag_start_point.x, y:drag_start_point.y-24 });
      // text.font({anchor: 'middle', size: 30, family: 'Helvetica'});
      box_group.add(text);


      _this.current_image.marks.push({name: element_name, svg_element: box_group, selected: false});
      drag_draw_element = null;
    });


    if(this.current_image == null) {
      this.selectImage(this.images[0]);
    }

  },
  methods: {
    toggleMark: function(selectedMark) {
      var element_rect = selectedMark.svg_element.get(0);
      if(selectedMark.selected) {
        selectedMark.selected = false;
        element_rect.stroke({ width: 2, color: '#000'});
      } else {

        this.current_image.marks.forEach(item =>{
          if(item != selectedMark) {
            item.selected = false;
            item.svg_element.get(0).stroke({ width: 2, color: '#000'});
          } else {
            selectedMark.selected = false;
            element_rect.stroke({ width: 2, color: '#FF9900'});
          }
        });

      }
      
    },

    removeMark: function(mark, index) {
      mark.svg_element.remove();
      this.$delete(this.current_image.marks, index); 
    },

    selectMarkCategory: function(mark, event){
        console.log("selectMarkCategory ", event.target.value, mark.name);
        //console.log(mark.svg_element.get(1));
        var c_id = event.target.value;
        var c_object = this.mark_categories.find(function(category){
           return category.id == c_id;
        });
        
        mark.svg_element.get(1).text(c_object.name);
    },

    selectImage: function(image_object) {
      console.log("Loading ", image_object.url);
      if(this.current_image == null || this.current_image.url != image_object.url) {

        // Remove old svg marks first.
        if(this.current_image != null) {
          this.current_image.marks.forEach(item =>{
            item.svg_element.remove();
          });
        }

        if(image_object.marks.length > 0) {

          image_object.marks.forEach(item =>{
            item.svg_element.addTo(this.svg_draw);
          });
        }
        
        this.current_image = image_object;
        this.svg_bg_image.load(image_object.url);  
      } else {
        console.log("Same image, not load again.");
      }
    
    } // / selectImage
  }
  }); // new Vue

});
