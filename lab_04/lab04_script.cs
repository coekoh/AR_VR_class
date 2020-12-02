using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class lab04_script : MonoBehaviour
{
    // Start is called before the first frame update

    private Mesh courageMesh;
    private Vector3[] vertices;
    private Vector2[] courageUV;
    private int[] triangle;


    void Start()
    {
        courageMesh = new Mesh();
        courageMesh.Clear();

        // Create vertices and triangle

        vertices = new Vector3[41 * 41];

        int point = 0;
        for (float i = -2.5f; i <= 2.5f; i += 0.125f)
        {
            for (float j = -2.5f; j <= 2.5f; j += 0.125f)
            {
                vertices[point] = new Vector3(j, i, 0);
                point++;
            }
        }


        // Declare UV component and assign to Material

        courageUV = new Vector2[41 * 41];
        int index = 0;
        for (float i = 0f; i <= 1.0f; i += 0.025f)
        {
            for (float j = 0f; j <= 1.0f; j += 0.025f)
            {
                courageUV[index] = new Vector2(j, i);
                index++;
            }
        }

        //create triangle
        triangle = new int[40*40*6];


        point = 0;
        for (int i = 0; i < 40; i++)
        {
            for (int j = 0; j < 40; j++)
            {
                int a = (i * 41) + j;
                int b = (i * 41) + j + 1;
                int c = a + 41 + 1;

                 a = 41 * i + j;
                 b = 41 * (i + 1) + j;
                 c = j + 1 + i * 41; 

                triangle[point++] = a;
                triangle[point++] = b;
                triangle[point++] = c;
                triangle[point++] = a + 41;
                triangle[point++] = b+1;
                triangle[point++] = c;

            }
         }




        //assign vertices and triangles to mesh
        courageMesh.vertices = vertices;
        courageMesh.triangles = triangle;
        courageMesh.uv = courageUV;
        

        // Recalculate bounds and normals
        courageMesh.RecalculateNormals();
        courageMesh.RecalculateBounds();

        GetComponent<MeshFilter>().mesh = courageMesh;
   
    }

    // Update is called once per frame
    void Update()
    {
        for (int i = 0; i < vertices.Length; i++)
        {
           vertices[i].z = Mathf.Cos(Mathf.PI * vertices[i].x) * Mathf.Cos(Mathf.PI * vertices[i].y) * Mathf.Sin(2 * Time.time);
        }
        courageMesh.vertices = vertices;
        courageMesh.RecalculateNormals();
        courageMesh.RecalculateBounds();
    }
}
