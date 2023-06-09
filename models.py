from app import db


class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    out_edges = db.relationship('Edge', back_populates='start_node', foreign_keys='Edge.start_node_id')
    in_edges = db.relationship('Edge', back_populates='end_node', foreign_keys='Edge.end_node_id')
    is_custom = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    
    def __repr__(self):
        return f"<Node {self.title} ({self.x};{self.y})>"
    
    def edges(self):
        return [
            *self.in_edges,
            *self.out_edges
        ]
    
    def neighbours(self):
        ns = set()
        for edge in self.in_edges:
            ns.add(edge.start_node)
        
        for edge in self.out_edges:
            ns.add(edge.end_node)
        
        return list(ns)

    @staticmethod
    def compose_edges(nodes):
        edges = []
        for i in range(len(nodes)-1):
            edge = Edge.query.filter_by(start_node=nodes[i], end_node=nodes[i+1]).first()
            edge = Edge.query.filter_by(start_node=nodes[i+1], end_node=nodes[i]).first() if not edge else edge
            edges.append(edge)
        
        return edges
    
    def distance_to(self, other):
        return min([edge.weight if edge else None for edge in Node.compose_edges([self, other])])


class Edge(db.Model):
    __tablename__ = 'edges'
    id = db.Column(db.Integer, primary_key=True)
    start_node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    end_node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    weight = db.Column(db.Float)
    start_node = db.relationship('Node', back_populates='out_edges', foreign_keys=[start_node_id], lazy='joined')
    end_node = db.relationship('Node', back_populates='in_edges', foreign_keys=[end_node_id], lazy='joined')
    is_custom = db.Column(db.Boolean, default=False)


    @staticmethod
    def calculate_overall_distance(edges):
        return sum([edge.weight for edge in edges])

    def __repr__(self):
        return f"<Edge {self.start_node.title}-{self.end_node.title} with weight {self.weight}>"
