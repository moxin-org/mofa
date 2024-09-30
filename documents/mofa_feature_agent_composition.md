# 模法3: 智能体组合（Composition）

组合是将各元素拼接形成新事物的方法和过程，在组合的过程中，不涉及元素的实际结合或变化。组合是松耦合的，具有可逆行和可叠加的特性，比如乐高玩具，可以将形状不同的乐高积木通过组合的方式构建成各式各样的物体。这些物体还可以通过进一步的组合形成更加复杂的物体。组合的物体也可以通过拆解的过程，还原成各元素。

为了更好地理解组合，我们还可以对比一下事物形成的方法，比如：

化合（Compound)：化合是多种元素发生了变化和进行了实际的结合，形成一种新的物质的方法和过程。过程中，元素发生了变化，紧密耦合的（我中有你，你中有我），复合过程不具备可逆性和可叠加性。比如蛋糕烘焙，面粉、糖、奶油，鸡蛋等元素，经过一个烘焙的复合过程成为蛋糕。而用几个小蛋糕烘焙成更大蛋糕或将蛋糕中的糖，鸡蛋等元素分解还原出来，是非常困难的。

![Image](https://mmbiz.qpic.cn/mmbiz_png/ibqbukt6PTv7GgGOVgGIQgKB7nIRZrSOfMSpIjbjmd4qnoJ2dmzBbtSSTK9VC7BER5uA2hvNECfOY378O667ibjw/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

图：组合，化合和混合的比较

混合（Mix)：混合是将多种元素通过物理方式放在一起。虽然混合的过程也存在可逆星河可叠加性，但这种方法，各元素之间并没有发生联系，并没有产生新的事物，而是形成了元素的集合。比如：将苹果和橙子放到了一起，我们得到的是苹果和橙子的集合。

通过MoFA，基于组合的方法和过程，AI应用开发者可以构建AI智能体，也可以将现有的智能体进行创造性的组合，从而形成具有新功能或更加强大的智能体。因为MoFA，智能体的开发变得过程简单，模块化，逻辑清晰，可扩展，可重用。

![Image](https://mmbiz.qpic.cn/mmbiz_png/ibqbukt6PTv7GgGOVgGIQgKB7nIRZrSOf0xDict8nR24OHOR4HvWlcniaRl6SO1UJLXibmLwrXUjiasr4hsiaPSq67hg/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

图：在MoFA里，可以将多个Agent组合在一起，形成一个功能更加强大的超级智能体