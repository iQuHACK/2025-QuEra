## Circuit implementation

Decomposition of the given circuits into the native gate language of our neutral atom computer was a significant portion of the challenge this year. To ensure that we created accurate, efficient circuits, we followed three tenets for our circuit construction:

**Construction of complex gates using our native gate set**: For this challenge, we were permitted to use three distinct gates: a CZ gate, a rotation around the Z axis, and a rotation around an axis in the XY plane. However, we were challenged to implement gates which were not immediately included in this set. To do this, we constructed necessary gates out of our limited set.
For example, the CNOT gate can be constructed using a CZ gate surrounded by Hadamards on the target qubit. Hadamards, in turn, can be implemented as a 90º rotation around the Y-axis, followed by a 180º rotation around the X-axis. By leveraging our gate set in imaginative ways, we were able to construct many arbitrary gates
![alt text](assets/arbitrary.png)
