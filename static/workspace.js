      var app = new Vue({
        el: '#app',
        data: {
          message: 'Hello Vue!',
          mark_elements: []
        }, 
        methods: {
          toggleElement: function(selectedElement) {
            if(selectedElement.selected) {
              selectedElement.selected = false;
              selectedElement.element.stroke({ width: 2, color: '#000'});
            } else {

              this.mark_elements.forEach(item =>{
                if(item != selectedElement) {
                  item.selected = false;
                  item.element.stroke({ width: 2, color: '#000'});
                } else {
                  selectedElement.selected = false;
                  selectedElement.element.stroke({ width: 2, color: '#FF9900'});
                }
              });

            }
            
          }
        }
      });

        var drawa = SVG().addTo('#drawing').size(900, 500);

        var drag_start = false;
        var drag_draw_element = null;
        var drag_start_point = {x:-1, y:-1};
        var drag_end_point = {x:-1, y:-1};
        var drag_new_rect = false;

        drawa.mousedown(function(e) {
          var point = {x: e.offsetX, y: e.offsetY};
          console.log(e, point.x, point.y);
          drag_start = true;
          drag_start_point = point;
        });

        drawa.mousemove(function(e) {
          var current_point = {x: e.offsetX, y: e.offsetY};
          if(drag_start) {
            var points_5 = [[drag_start_point.x,drag_start_point.y], [current_point.x,drag_start_point.y], [current_point.x,current_point.y], [drag_start_point.x, current_point.y], [drag_start_point.x,drag_start_point.y]];
            if(drag_draw_element != null) {
              drag_draw_element.remove();
            }
            drag_draw_element = drawa.polyline(points_5).fill('none').stroke({ width: 2, color: '#000'});
          }
        });

        drawa.mouseup(function(e) {
          console.log(e, e.x, e.y);
          drag_end_point = {x: e.x, y: e.y};
          console.log(drag_end_point);

          drag_start = false;
          var mark_count = app.mark_elements.length;
          app.mark_elements.push({name: "Mark "+mark_count, element: drag_draw_element, selected: false});
          drag_draw_element = null;
        });

        var image = drawa.image('/static/fruits.jpg');