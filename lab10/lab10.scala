
val myNumbers = List(1, 2, 5, 4, 7, 3)


def cube(a: Int): Int = a * a * a

def factorial(n: Int): Int = {
  var i = 1;
  var res = 1;
  while (i <= n) {
    res = res * i;
    i += 1;
  }
  return res
}


def factorial(n: Int): Int = {
    if (n==0) 1 else n*factorial(n-1)
}

val fact = myNumbers.map(factorial).sum


val vertexArray = Array(
  (1L, ("Alice", 28)),
  (2L, ("Bob", 27)),
  (3L, ("Charlie", 65)),
  (4L, ("David", 42)),
  (5L, ("Ed", 55)),
  (6L, ("Fran", 50))
)
val edgeArray = Array(
  Edge(2L, 1L, 7),
  Edge(2L, 4L, 2),
  Edge(3L, 2L, 4),
  Edge(3L, 6L, 3),
  Edge(4L, 1L, 1),
  Edge(5L, 2L, 2),
  Edge(5L, 3L, 8),
  Edge(5L, 6L, 3)
)

graph.vertices.filter { case (id, (name, age)) => age >= 30 }.foreach { case (id, (name, age)) => println(name)}


graph.triplets.foreach { t =>
 /**
   * Triplet has the following Fields:
   *   triplet.srcAttr: (String, Int) // triplet.srcAttr._1 is the name
   *   triplet.dstAttr: (String, Int) // The dst vertex property
   *   triplet.attr: Int // The edge property
   *   triplet.srcId: VertexId
   *   triplet.dstId: VertexId
   */
   println(t.srcAttr._1 + " likes "  +t.dstAttr._1)
}

degreeGraph.vertices.filter {
  case (id, u) => u.inDeg == u.outDeg
}.foreach(println(_))



################# PT 2 ##################
// Change labshome to the appropriate value for your computer
val labshome = "/Users/t-rex-Box/Desktop/work/cs194/lab10"
val edgeGraph = GraphLoader.edgeListFile(sc, s"${labshome}/edges.txt")


val verts = sc.textFile(s"${labshome}/verts.txt").map {l =>
  val lineSplits = l.split("\\s+")
  val id = lineSplits(0).trim.toLong
  val data = lineSplits.slice(1, lineSplits.length).mkString(" ")
  (id, data)
}

val g = edgeGraph.outerJoinVertices(verts)({ (vid, _, title) => title.getOrElse("xxxx")}).cache

val numEdges = g.edges.count()
val numVertices = g.vertices.count()

val maxDegree = g.inDegrees.map{ case (vid, data) => data}.reduce((x,y) => if (x > y) x else y)

val prs = g.staticPageRank(10)

val ranksAndVertices: Graph[(Double, String), Int] = g.outerJoinVertices(prs.vertices){
  (v, title, r) => (r.getOrElse(0.0) , title)
}

val top10 = ranksAndVertices.vertices.top(10)(Ordering.by((entry: (VertexId, (Double, String))) => entry._2._1)).mkString("\n")

val ccResult = g.connectedComponents()
ccResult.vertices.count


val ccSizes = ccResult.vertices.map { case (vid, data) => (data, 1) }.reduceByKey(_ + _)

ccSizes.map{ case (ccID, size) => size }.collect.sorted
ccResult.vertices.count
