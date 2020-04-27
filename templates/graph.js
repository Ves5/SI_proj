d3.json("{{url_for('static', filename='graph.json')}}", function (error, graph) {
    if (error) throw error;

    var iframe = d3.select("iframe");
    var svg = d3.select("svg");
    var select = document.querySelector("#list");
    var button = document.querySelector("#select");
    var svg_size = document.querySelector("#graph").getBoundingClientRect();
    var nodes_select = [];
    var links_select = [];

    // on click open pdf and start graph simulation
    button.addEventListener("click", selection);
    function selection() {
        iframe.attr("src", "http://127.0.0.1/pdf/" + graph.nodes[select.value].path);
        svg.style("visibility", "visible");
        nodes_select = [];
        links_select = [];
        [nodes_select, links_select] = findLinked(select.value);
        var k;
        for (k = 0; k < links_select.length; k++){
            var index;
            for(index = 0; index < nodes_select.length; index++){
                if (links_select[k].source == nodes_select[index])
                    links_select[k].source = index;
                if (links_select[k].target == nodes_select[index])
                    links_select[k].target = index;
            }
        }
        sim();
    }

    // filling list
    for (const node of graph.nodes) {
        let option = document.createElement("option");
        option.textContent = node.name;
        option.value = node.id;
        select.appendChild(option);
    }
    // function to find all nodes that link to chosen node
    function findLinked(node_id){
        let arr = [];
        let links = [];
        arr.push(graph.nodes[node_id]);
        for(const l of graph.links){
            if(l.source == node_id){
                arr.push(graph.nodes[l.target]);
                links.push(l);
            }
            if(l.target == node_id){
                arr.push(graph.nodes[l.source]);
                links.push(l);
            }
        }
        // arr stores ids of all nodes that link to the chosen one and itself
        return [arr, links];
    }

    function sim(){
        var radius = 12;

        function linkColour(d) {
            return d3.rgb(255 - d.weight * 255, 255 - d.weight * 255, 255 - d.weight * 255);
        }

        var link = svg.selectAll("line")
            .data(links_select)
            .enter().append("line")
            .style("stroke", "#111")
            .style("stroke-width", "2px")
            .style("stroke", function (d) {
                return linkColour(d);
            });

        var force = d3.layout.force()
            .gravity(.05)
            .charge(-300)
            .linkDistance(function (d) {
                return 20 / d.weight;
            })
            .size([svg_size.width, svg_size.height]);

        var node = svg.selectAll("circle")
            .data(nodes_select)
            .enter().append("circle")
            .attr("r", radius - .75)
            .style("fill", "#999")
            .style("stroke", "#111")
            .call(force.drag)
            .on("click", function (d) { iframe.attr("src", "http://127.0.0.1/pdf/" + d.path) });
        //.on("dblclick", function(){ dblclick(d3.select(this)); })


        /*var texts = svg.selectAll("text.label")
            .data(nodes_select)
            .enter().append("text")
            .attr("class", "label")
            .attr("fill", "black")
            .attr("dx", "1.05em")
            .attr("dy", ".28em")
            .text(function (d) { return d.path; }); //skrócona nazwa*/

        node.append("title")
            .text(function (d) { return d.name; });


        force
            .nodes(nodes_select)
            .links(links_select)
            .on("tick", tick)
            .start();

        resize();
        d3.select(window).on("resize", resize);

        function tick() {
            node.attr("cx", function (d) { return d.x = Math.max(radius, Math.min(svg_size.width - radius, d.x)); })
                .attr("cy", function (d) { return d.y = Math.max(radius, Math.min(svg_size.height - radius, d.y)); });

            link.attr("x1", function (d) { return d.source.x; })
                .attr("y1", function (d) { return d.source.y; })
                .attr("x2", function (d) { return d.target.x; })
                .attr("y2", function (d) { return d.target.y; });

            /*texts.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });*/
        }


        function resize() {
            svg_size = document.querySelector("#graph").getBoundingClientRect();
            force.size([svg_size.width, svg_size.height]).resume();
        }
    }
});