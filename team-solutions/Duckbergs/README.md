## Circuit implementation

Decomposition of the given circuits into the native gate language of our neutral atom computer was a significant portion of the challenge this year. To ensure that we created accurate, efficient circuits, we followed three tenets for our circuit construction:

**1. Construction of complex gates using our native gate set**: For this challenge, we were permitted to use three distinct gates: a CZ gate, a rotation around the Z axis, and a rotation around an axis in the XY plane. However, we were challenged to implement gates which were not immediately included in this set. To do this, we constructed necessary gates out of our limited set.
For example, the CNOT gate can be constructed using a CZ gate surrounded by Hadamards on the target qubit. Hadamards, in turn, can be implemented as a 90º rotation around the Y-axis, followed by a 180º rotation around the X-axis. By leveraging our gate set in imaginative ways, we were able to construct many arbitrary gates
<br>
![alt text](assets/arbitrary.png)

**2. The use of commutation identities to simplify the circuit**: Because we were forced to enact operations with a small collection of simple gates, our circuits were often left with many single-qubit gates that would have been very costly to implement. As such, we took advantage of commutation relations to simplify things. For example, a rotation of an arbitrary angle around the Z-axis, when surrounded by Hadamard gates, is equivalent to that same rotation around the X-axis. Similarly, if an operator is immediately followed by its conjugate transpose, the pair will cancel out and we can disregard them entirely.

**3. Emphasis on global gates**: In the cost function of our circuits, global gates have a much lower cost than a gate on an individual qubit. As such, whenever possible, we leveraged global gates to make our circuit more efficient. Even if we didn’t necessarily need to conduct an operation on all of our qubits—if, for example, we only needed to implement an x-rotation around three of our four qubits— we found that it was often still more efficient to enact a global rotation and then use single-qubit gates to “correct” the qubits which didn’t need that operation.

However, constructing an efficient circuit was not the only challenge. We also needed to implement our circuit in a way which reduced the time spent on the neutral-atom simulator. To do this, we focused on two approaches:

**1. Placing our “central nodes” near the center**: In many of our circuits, we found that many qubits would all become entangled through operations with some singular qubit (or sometimes multiple). We call that qubit the “central node” When placing our qubits in storage, we usually placed the central node near the center of our qubit distribution, so that no qubit would need to travel far to conduct an entanglement operation with it.

**2. Grouping moves**: Again, time is of the essence when implementing these operations. As such, while moving one atom at a time would be the much easier solution, doing so would be extremely costly for our runtime. As such, we structured our circuit implementations such that we could move many atoms concurrently without them overlapping. For example, if we knew that atom #4 would need to pass to the left over atom #3 to reach its new entangling partner, but atom #3 also needed to change positions, we would structure our circuit so that atom #3’s final destination was also to the left. In this way, we could move atoms #4 and #3 concurrently to reduce movement time.

# Challenge Solutions

1. Question 1.1
   time: 5.399560555969611
   ntouches: 4
   nmoves: 2
   apply_cz: 2
   apply_local_xy: 4
   overall: 8.279912111193923
   ![1.1](assets/q1.1.png)
2. Question 1.2
   time: 18.400656362432144
   ntouches: 10
   nmoves: 8
   apply_cz: 6
   apply_local_xy: 9
   apply_local_rz: 2
   overall: 23.180131272486427
   ![1.2](assets/q1.2.png)
3. Question 2
   time: 7.42558007523081
   ntouches: 6
   nmoves: 3
   apply_local_xy: 6
   apply_cz: 6
   apply_global_xy: 6
   overall: 15.405116015046163
   ![2](assets/q2.png)
4. Question 3
   N/A
   ![3](assets/q3.png)
5. Question 4
   time: 26.51189099066703
   ntouches: 14
   nmoves: 8
   apply_global_xy: 36
   apply_local_xy: 10
   apply_cz: 8
   overall: 30.222378198133406
   ![4](assets/q4.png)
6. Question 5
   time: 21.23919760197064
   ntouches: 17
   nmoves: 7
   apply_global_xy: 28
   apply_local_xy: 10
   apply_cz: 11
   overall: 34.40783952039413
   ![5](assets/q5.png)
