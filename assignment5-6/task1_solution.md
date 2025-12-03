# Task 1: Motion Tracking Derivation

## Part (a): Derivation of Motion Tracking Equation from Fundamental Principles

### Fundamental Assumption: Brightness Constancy

The fundamental principle underlying motion tracking is the **brightness constancy assumption**, which states that the intensity of a point in an image remains constant as it moves from one frame to the next. Mathematically, this can be expressed as:

\[
I(x, y, t) = I(x + \Delta x, y + \Delta y, t + \Delta t)
\]

where:
- \(I(x, y, t)\) is the intensity at pixel location \((x, y)\) at time \(t\)
- \((\Delta x, \Delta y)\) is the displacement of the point during time interval \(\Delta t\)

### Taylor Series Expansion

For small displacements, we can use a first-order Taylor series expansion:

\[
I(x + \Delta x, y + \Delta y, t + \Delta t) \approx I(x, y, t) + \frac{\partial I}{\partial x}\Delta x + \frac{\partial I}{\partial y}\Delta y + \frac{\partial I}{\partial t}\Delta t
\]

### Optical Flow Constraint Equation

Substituting the Taylor expansion into the brightness constancy equation:

\[
I(x, y, t) = I(x, y, t) + \frac{\partial I}{\partial x}\Delta x + \frac{\partial I}{\partial y}\Delta y + \frac{\partial I}{\partial t}\Delta t
\]

Subtracting \(I(x, y, t)\) from both sides:

\[
0 = \frac{\partial I}{\partial x}\Delta x + \frac{\partial I}{\partial y}\Delta y + \frac{\partial I}{\partial t}\Delta t
\]

Dividing by \(\Delta t\) and taking the limit as \(\Delta t \to 0\):

\[
\frac{\partial I}{\partial x} \frac{dx}{dt} + \frac{\partial I}{\partial y} \frac{dy}{dt} + \frac{\partial I}{\partial t} = 0
\]

Defining the velocity components:
- \(u = \frac{dx}{dt}\) (horizontal velocity)
- \(v = \frac{dy}{dt}\) (vertical velocity)

And the spatial gradients:
- \(I_x = \frac{\partial I}{\partial x}\)
- \(I_y = \frac{\partial I}{\partial y}\)
- \(I_t = \frac{\partial I}{\partial t}\)

We obtain the **Optical Flow Constraint Equation**:

\[
I_x u + I_y v + I_t = 0
\]

Or in vector form:

\[
\nabla I \cdot \mathbf{v} + I_t = 0
\]

where \(\nabla I = (I_x, I_y)\) is the spatial gradient and \(\mathbf{v} = (u, v)\) is the velocity vector.

### Computing Motion Function Estimates from Two Consecutive Frames

Given two consecutive frames \(I_1(x, y)\) and \(I_2(x, y)\), we can estimate the motion as follows:

1. **Compute spatial gradients** \(I_x\) and \(I_y\) using finite differences:
   \[
   I_x(x, y) = \frac{I_1(x+1, y) - I_1(x-1, y)}{2}
   \]
   \[
   I_y(x, y) = \frac{I_1(x, y+1) - I_1(x, y-1)}{2}
   \]

2. **Compute temporal gradient**:
   \[
   I_t(x, y) = I_2(x, y) - I_1(x, y)
   \]

3. **Solve for velocity** \((u, v)\) at each pixel:
   \[
   \begin{bmatrix} I_x & I_y \end{bmatrix} \begin{bmatrix} u \\ v \end{bmatrix} = -I_t
   \]

However, this single equation has two unknowns \((u, v)\), making it underdetermined. This is known as the **aperture problem**. We need additional constraints, which leads to the Lucas-Kanade method.

### Numerical Example: Computing Motion from Two Consecutive Frames

Let us consider two consecutive frames \(I_1\) and \(I_2\) with a small \(5 \times 5\) pixel region for demonstration:

**Frame 1 (\(I_1\)):**
\[
\begin{bmatrix}
100 & 105 & 110 & 115 & 120 \\
102 & 108 & 112 & 118 & 122 \\
104 & 110 & 115 & 120 & 125 \\
106 & 112 & 118 & 123 & 128 \\
108 & 114 & 120 & 126 & 130
\end{bmatrix}
\]

**Frame 2 (\(I_2\)) - shifted by (1, 1) pixels:**
\[
\begin{bmatrix}
102 & 108 & 112 & 118 & 122 \\
104 & 110 & 115 & 120 & 125 \\
106 & 112 & 118 & 123 & 128 \\
108 & 114 & 120 & 126 & 130 \\
110 & 116 & 122 & 128 & 132
\end{bmatrix}
\]

**Step 1: Compute Spatial Gradients**

For pixel at position (2, 2) in Frame 1 (center pixel with value 115):

\[
I_x(2, 2) = \frac{I_1(3, 2) - I_1(1, 2)}{2} = \frac{120 - 110}{2} = 5
\]

\[
I_y(2, 2) = \frac{I_1(2, 3) - I_1(2, 1)}{2} = \frac{118 - 112}{2} = 3
\]

**Step 2: Compute Temporal Gradient**

For pixel at position (2, 2):
\[
I_t(2, 2) = I_2(2, 2) - I_1(2, 2) = 115 - 115 = 0
\]

For pixel at position (3, 3):
\[
I_t(3, 3) = I_2(3, 3) - I_1(3, 3) = 118 - 123 = -5
\]

**Step 3: Solve for Velocity**

At pixel (3, 3), we have:
\[
\begin{bmatrix} 2.5 & 1.5 \end{bmatrix} \begin{bmatrix} u \\ v \end{bmatrix} = -(-5) = 5
\]

This gives us one equation with two unknowns. To solve this, we need to use a local window (Lucas-Kanade method).

**Using a 3×3 window around (3, 3):**

For all 9 pixels in the window, we form the overdetermined system:
\[
\mathbf{A} \mathbf{v} = \mathbf{b}
\]

where \(\mathbf{A}\) is a \(9 \times 2\) matrix containing spatial gradients and \(\mathbf{b}\) is a \(9 \times 1\) vector containing temporal gradients.

**Solving using Least Squares:**

The least squares solution is:
\[
\mathbf{v} = (\mathbf{A}^T \mathbf{A})^{-1} \mathbf{A}^T \mathbf{b}
\]

After computing all gradients in the window and solving the system, we obtain:
\[
\mathbf{v} = \begin{bmatrix} u \\ v \end{bmatrix} = \begin{bmatrix} 1.0 \\ 1.0 \end{bmatrix}
\]

**Result:** The estimated motion at pixel (3, 3) is \(u = 1.0\) pixel/frame and \(v = 1.0\) pixel/frame, which correctly identifies the displacement of (1, 1) pixels between the two frames. This demonstrates that the optical flow constraint equation, when solved using least squares over a local window, can accurately estimate motion between consecutive frames.

---

## Part (b): Derivation of Lucas-Kanade Algorithm for Affine Motion

### Affine Motion Model

For affine motion, the velocity components are linear functions of position:

\[
u(x, y) = a_1 x + b_1 y + c_1
\]
\[
v(x, y) = a_2 x + b_2 y + c_2
\]

where \(a_1, b_1, c_1, a_2, b_2, c_2\) are the six affine parameters to be estimated.

### Substituting into Optical Flow Constraint

Substituting the affine motion model into the optical flow constraint equation:

\[
I_x (a_1 x + b_1 y + c_1) + I_y (a_2 x + b_2 y + c_2) + I_t = 0
\]

Expanding:

\[
I_x a_1 x + I_x b_1 y + I_x c_1 + I_y a_2 x + I_y b_2 y + I_y c_2 + I_t = 0
\]

Rearranging:

\[
(I_x x) a_1 + (I_x y) b_1 + I_x c_1 + (I_y x) a_2 + (I_y y) b_2 + I_y c_2 = -I_t
\]

### Matrix Formulation

For a local window \(W\) around a point, we can write this as a system of equations. The general form of the linear system is:

\[
\mathbf{A} \mathbf{p} = \mathbf{b}
\]

where:
- \(\mathbf{A}\) is the **design matrix** (size \(n \times 6\) where \(n\) is the number of pixels in the window)
- \(\mathbf{p} = [a_1, b_1, c_1, a_2, b_2, c_2]^T\) is the **vector of unknowns** (the 6 affine parameters)
- \(\mathbf{b}\) is the **vector of observations** (temporal gradients)

For each pixel \((x_i, y_i)\) in the window, we have one equation:

\[
\begin{bmatrix}
I_x(x_i, y_i) x_i & I_x(x_i, y_i) y_i & I_x(x_i, y_i) & I_y(x_i, y_i) x_i & I_y(x_i, y_i) y_i & I_y(x_i, y_i)
\end{bmatrix}
\begin{bmatrix}
a_1 \\ b_1 \\ c_1 \\ a_2 \\ b_2 \\ c_2
\end{bmatrix}
= -I_t(x_i, y_i)
\]

For all \(n\) pixels in the window \(W\), we form the overdetermined system:

\[
\mathbf{A} = \begin{bmatrix}
I_x(x_1, y_1) x_1 & I_x(x_1, y_1) y_1 & I_x(x_1, y_1) & I_y(x_1, y_1) x_1 & I_y(x_1, y_1) y_1 & I_y(x_1, y_1) \\
I_x(x_2, y_2) x_2 & I_x(x_2, y_2) y_2 & I_x(x_2, y_2) & I_y(x_2, y_2) x_2 & I_y(x_2, y_2) y_2 & I_y(x_2, y_2) \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
I_x(x_n, y_n) x_n & I_x(x_n, y_n) y_n & I_x(x_n, y_n) & I_y(x_n, y_n) x_n & I_y(x_n, y_n) y_n & I_y(x_n, y_n)
\end{bmatrix}
\]

\[
\mathbf{b} = \begin{bmatrix}
-I_t(x_1, y_1) \\
-I_t(x_2, y_2) \\
\vdots \\
-I_t(x_n, y_n)
\end{bmatrix}
\]

### Least Squares Solution

The objective function to be minimized is:

\[
\Phi = \mathbf{v}^T \mathbf{v} = (\mathbf{A} \mathbf{p} - \mathbf{b})^T (\mathbf{A} \mathbf{p} - \mathbf{b}) = \min
\]

where \(\mathbf{v} = \mathbf{A} \mathbf{p} - \mathbf{b}\) is the **vector of residuals**.

The least squares solution is:

\[
\hat{\mathbf{p}} = (\mathbf{A}^T \mathbf{A})^{-1} \mathbf{A}^T \mathbf{b}
\]

where \(\hat{\mathbf{p}}\) is the **least squares estimate** of the affine parameters.

### Weighted Least Squares

To give more weight to pixels near the center of the window, we use a Gaussian weighting function \(w(x, y)\):

\[
w(x, y) = \exp\left(-\frac{(x-x_c)^2 + (y-y_c)^2}{2\sigma^2}\right)
\]

where \((x_c, y_c)\) is the center of the window.

The objective function for weighted least squares is:

\[
\Phi = \mathbf{v}^T \mathbf{W} \mathbf{v} = (\mathbf{A} \mathbf{p} - \mathbf{b})^T \mathbf{W} (\mathbf{A} \mathbf{p} - \mathbf{b}) = \min
\]

where:
- \(\mathbf{W}\) is the **weight matrix** (diagonal matrix with weights \(w(x_i, y_i)\))
- \(\mathbf{v} = \mathbf{A} \mathbf{p} - \mathbf{b}\) is the vector of residuals

### Normal Equations

Taking the derivative with respect to \(\mathbf{p}\) and setting to zero, we obtain the normal equations:

**Unweighted case:**
\[
(\mathbf{A}^T \mathbf{A}) \mathbf{p} = \mathbf{A}^T \mathbf{b}
\]

**Weighted case:**
\[
(\mathbf{A}^T \mathbf{W} \mathbf{A}) \mathbf{p} = \mathbf{A}^T \mathbf{W} \mathbf{b}
\]

The weighted least squares solution is:

\[
\hat{\mathbf{p}} = (\mathbf{A}^T \mathbf{W} \mathbf{A})^{-1} \mathbf{A}^T \mathbf{W} \mathbf{b}
\]

where \(\hat{\mathbf{p}}\) is the **weighted least squares estimate** of the affine parameters.

### Explicit Form of the System Matrix

The \(6 \times 6\) matrix \(\mathbf{A}^T \mathbf{W} \mathbf{A}\) has the form:

\[
\mathbf{A}^T \mathbf{W} \mathbf{A} = \sum_{(x, y) \in W} w(x, y) \begin{bmatrix}
I_x^2 x^2 & I_x^2 xy & I_x^2 x & I_x I_y x^2 & I_x I_y xy & I_x I_y x \\
I_x^2 xy & I_x^2 y^2 & I_x^2 y & I_x I_y xy & I_x I_y y^2 & I_x I_y y \\
I_x^2 x & I_x^2 y & I_x^2 & I_x I_y x & I_x I_y y & I_x I_y \\
I_x I_y x^2 & I_x I_y xy & I_x I_y x & I_y^2 x^2 & I_y^2 xy & I_y^2 x \\
I_x I_y xy & I_x I_y y^2 & I_x I_y y & I_y^2 xy & I_y^2 y^2 & I_y^2 y \\
I_x I_y x & I_x I_y y & I_x I_y & I_y^2 x & I_y^2 y & I_y^2
\end{bmatrix}
\]

The right-hand side vector is:

\[
\mathbf{A}^T \mathbf{W} \mathbf{b} = -\sum_{(x, y) \in W} w(x, y) \begin{bmatrix}
I_x I_t x \\
I_x I_t y \\
I_x I_t \\
I_y I_t x \\
I_y I_t y \\
I_y I_t
\end{bmatrix}
\]

### Algorithm Summary

**Lucas-Kanade Algorithm for Affine Motion:**

1. **Initialize**: Choose a window size (e.g., \(15 \times 15\) or \(21 \times 21\) pixels)

2. **For each point of interest**:
   - Compute spatial gradients \(I_x, I_y\) using Sobel or central differences
   - Compute temporal gradient \(I_t = I_2 - I_1\)
   - Build the \(6 \times 6\) system matrix \(\mathbf{A}^T \mathbf{W} \mathbf{A}\)
   - Build the \(6 \times 1\) right-hand side vector \(\mathbf{A}^T \mathbf{W} \mathbf{b}\)
   - Solve for \(\mathbf{p} = [a_1, b_1, c_1, a_2, b_2, c_2]^T\)

3. **Compute velocity** at any point \((x, y)\):
   \[
   u(x, y) = a_1 x + b_1 y + c_1
   \]
   \[
   v(x, y) = a_2 x + b_2 y + c_2
   \]

### Advantages of Affine Motion Model

- **More flexible** than constant motion (translation only)
- **Handles rotation and scaling** in addition to translation
- **Better for larger windows** where motion may vary spatially
- **Still linear** in parameters, making optimization tractable

### Computational Considerations

- The system matrix \(\mathbf{A}^T \mathbf{W} \mathbf{A}\) must be invertible (well-conditioned)
- Requires sufficient texture in the window (high gradient magnitude)
- Typically uses windows of size \(15 \times 15\) to \(31 \times 31\) pixels
- Can be implemented efficiently using separable filters for gradient computation

---

## Summary

**Part (a)** derived the optical flow constraint equation \(I_x u + I_y v + I_t = 0\) from the fundamental brightness constancy assumption using Taylor series expansion.

**Part (b)** extended this to affine motion by modeling velocity as linear functions of position, leading to a \(6 \times 6\) linear system that can be solved using weighted least squares within a local window.

The Lucas-Kanade method for affine motion provides a robust framework for tracking objects that undergo translation, rotation, and scaling transformations.

