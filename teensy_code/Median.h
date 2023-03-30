void swap(int *p,int *q) {
   int t;

   t=*p;
   *p=*q;
   *q=t;
}

void sort(int a[],int n) {
   int i,j,temp;

   for(i=0;i<n-1;i++) {
      for(j=0;j<n-i-1;j++) {
         if(a[j]>a[j+1])
            swap(&a[j],&a[j+1]);
      }
   }
}

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}



void loop() {
   int a[] = {150,200,0};
   int n = 3;
   int sum,i;

   sort(a,n);

   n = (n+1) / 2 - 1;  // -1 as array indexing in C starts from 0
   int avg = (a[0]+a[1]+a[2])/3;
   Serial.print("Median = ");
   Serial.println(a[n]);
   Serial.print("Average = ");
   Serial.println(avg);
   delay(5000);

}
