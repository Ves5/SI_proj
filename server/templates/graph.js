d3.json("{{url_for('json')}}", function (error, graph) {
    if (error) throw error;

    var iframe = d3.select("iframe");
    var svg = d3.select("svg");
    var select = document.querySelector("#list");
    var button = document.querySelector("#select");
    var svg_size = document.querySelector("#graph").getBoundingClientRect();
    var links_orig = [];
    var minX = 1000;
    var minY = 1000;
    var first_double_click = true;
    // znajduje minimalny x i y
    for (node of graph.nodes)
    {
        if(node.x < minX)
            minX = node.x;
        if(node.y < minY)
            minY = node.y;
    }
    // przesuwa wszystkie wierzchołki o moduł z minimalnych wartości tak żeby każdy miał x >=0 i t >= 0
    for (let i = 0; i < graph.nodes.length; i++)
    {
        graph.nodes[i].x += Math.abs(minX);
        graph.nodes[i].y += Math.abs(minY);
    }
    var maxX = 0;
    var maxY = 0;
    // znajduje maksymale x i y
    for (node of graph.nodes)
    {
        if(node.x > maxX)
            maxX = node.x;
        if(node.y > maxY)
            maxY = node.y;
    }
    // przeskalowuje pozycję każdego wierzchołka tak żeby najpierw wartości były [0;1]
    // a potem żeby rozłozyły się na 2/3 wielkości svg
    // i przesuwa je o 1/5 długości/wysokości od górnej i lewej krawędzi
    for (let i = 0; i< graph.nodes.length; i++)
    {
        graph.nodes[i].x = (graph.nodes[i].x / maxX) * svg_size.width * 2/3 + svg_size.width * 1/5;
        graph.nodes[i].y = (graph.nodes[i].y / maxY) * svg_size.height * 2/3 + svg_size.height * 1/5;
    }
    let temp_graph = JSON.parse(JSON.stringify(graph)) //robienie kopii grafu
    var nodes_select = temp_graph.nodes;
    var links_select = temp_graph.links;
    // wyświetlenie
    sim();

    // po kliknięciu otwiera PDF oraz rozpoczyna symulację
    button.addEventListener("click", selection);
    function selection() {
        iframe.attr("src", "{{ request.url_root }}" +"pdf/" + graph.nodes[select.value].path);
        [nodes_select, links_select] = findLinked(select.value);
        links_orig = links_select.slice();
        first_double_click = false;
        // Zmiana indeksów WAŻNE
        // Przy wyświetlaniu jako parametry source i target w krawędzi należy podac indeksy w tablicy, na ktorych znajduje się dany wierzcholek
        // NIE CHODZI O ID ZAWARTE W WIERZCHOŁKU
        changeIndexes();
        sim();
    }
    

    function dblclick(node){
        let new_nodes = [];
        let new_links = [];
        if(first_double_click){
            first_double_click = false;
            [new_nodes, new_links] = findLinked(node.id);
            links_orig = [];
            nodes_select = [];
            links_select = [];
        }
        else{
            [new_nodes, new_links] = findLinkedNotSelected(node.id);
        }
        links_orig = links_orig.concat(new_links);
        nodes_select = nodes_select.concat(new_nodes);
        links_select = links_orig.slice();
        changeIndexes();
        sim();
    }

    function changeIndexes(){
        for (let k = 0; k < links_select.length; k++){
            source_change = false;
            target_change = false;
            for(index = 0; index < nodes_select.length; index++){
                if (links_select[k].source == nodes_select[index].id && source_change == false){
                    links_select[k].source = index;
                    source_change = true;
                }
                if (links_select[k].target == nodes_select[index].id && target_change == false){
                    links_select[k].target = index;
                    target_change = true;
                }
            }
        }
    }

    //lista z dokumentami
    for (const node of graph.nodes) {
        let option = document.createElement("option");
        option.textContent = node.name;
        option.value = node.id;
        select.appendChild(option);
    }
    
    //same as below but without nodes and links that are already displayed
    function findLinkedNotSelected(node_id){
        [nodes, links] = findLinked(node_id);
        let not_selected_nodes = [];
        not_selected_links = [];
        for (node of nodes){
            copy = true;
            for(n of nodes_select){
                if (node.id == n.id){
                    copy = false;
                    break;
                }
            }
            if (copy)
                not_selected_nodes.push(node);
        }
        for (link of links){
            copy = true;
            for(l of links_select){
                if (link.source == l.source && link.target == l.target){
                    copy = false;
                    break;
                }
            }
            if (copy)
                not_selected_links.push(link);
        }
        return [not_selected_nodes, not_selected_links];
    }

    // funkcja znajdująca węzły, które są połączone z wybranym węzłem
    function findLinked(node_id){
        let arr = [];
        let links = [];
        arr.push(graph.nodes[node_id]);
        for(const l of graph.links){
            if(l.source == node_id){
                arr.push(graph.nodes[l.target]);
                copy = Object.assign({}, l);
                links.push(copy);
            }
            if(l.target == node_id){
                arr.push(graph.nodes[l.source]);
                copy = Object.assign({}, l);
                links.push(copy);
            }
        }
        // zwraca tablicę z id węzłami i linkami
        return [arr, links];
    }

    function sim(){
        
        //usuniecie wszystkiego, co było wcześniej wyświetlone
        svg.selectAll('g').remove();
        svg.selectAll("line").remove();
        svg.selectAll("circle").remove();
        svg.selectAll("text.label").remove();

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
            .attr("cx", function(d){return d.x;})
            .attr("cy", function(d){return d.y;})
            .attr("id", function(d){ return d.id; })
            .attr("r", radius - .75)
            .style("fill", "#999")
            .style("stroke", "#111")
            .call(force.drag)
            .classed("fixed",function(d){ d.fixed = first_double_click;})
            .on("click", function (d) { iframe.attr("src", "{{ request.url_root }}" +"pdf/" + d.path) })
            .on("dblclick", function(d){ dblclick(d); });


        var texts = svg.selectAll("text.label")
            .data(nodes_select)
            .enter().append("text")
            .attr("class", "label")
            .attr("fill", "black")
            .attr("dx", "1.05em")
            .attr("dy", ".28em")
            .text(function (d) { return d.path; }); //skrócona nazwa

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

            texts.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
        }


        function resize() {
            svg_size = document.querySelector("#graph").getBoundingClientRect();
            force.size([svg_size.width, svg_size.height]).resume();
        }
    }
});