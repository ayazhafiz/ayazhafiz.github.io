fn cost(points: &[[f64; 2]], center: &[f64; 2]) -> f64 {
    points.iter().fold(0., |net, point| {
        let cost = (
            (center[0] - point[0]).powi(2) // `x` coordinates
            + (center[1] - point[1]).powi(2) // `y` coordinates
        ).sqrt();
        net + cost
    })
}

struct Delta {
    x: [i8; 4],
    y: [i8; 4],
}

fn geometric_center(points: &[[f64; 2]]) -> [f64; 2] {
    const DELTA: Delta = Delta {
        x: [-1, 0, 1, 0], // movement in `x` direction
        y: [0, 1, 0, -1], // movement in `y` direction
    };
    const EPSILON: f64 = 0.001; // some acceptable margin

    let arr_length = points.len() as f64;
    let mut center = points.iter().fold([0., 0.], |avg, point| {
        let x = avg[0] + (point[0] / arr_length);
        let y = avg[1] + (point[1] / arr_length);
        [x, y]
    }); // starts off as the median
    let mut step = 10.; // search radius
    let mut score = cost(&points, &center);

    while step > EPSILON {
        let mut improved = false;
        for i in 0..DELTA.x.len() {
            let _center = [
                center[0] + DELTA.x[i] as f64 * step,
                center[1] + DELTA.y[i] as f64 * step,
            ];
            let _score = cost(&points, &_center);

            if _score < score {
                center = _center;
                score = _score;
                improved = !improved;
                break;
            }
        }

        if !improved {
            step /= 2.;
        }
    }

    center
}

fn main() {
    let points = [[0., 0.], [0., 1.], [1., 0.]];
    let center = geometric_center(&points);
    println!("{:?}", center);
}
