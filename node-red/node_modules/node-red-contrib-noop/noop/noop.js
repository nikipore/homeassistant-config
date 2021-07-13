module.exports = function(RED) {
    function NoOpNode(n) {
        RED.nodes.createNode(this,n);
        var node = this;
        this.on('input', function(msg) {
            node.send(msg);
        });
    }
    RED.nodes.registerType("no-op",NoOpNode);
}

