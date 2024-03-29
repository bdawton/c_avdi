#include <SPI.h>
#include <SD.h>
#define chipSelect BUILTIN_SDCARD
#include "quickSort.h"
#include <limits.h>
#include "classifier_to_test_float_G1.h"
#define DATA_LEN 6000
#define FEATURE_LEN 5

File dataFile;
File labelFile;

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect.
  }
  Serial.print("Initializing SD card...");
  if (!SD.begin(chipSelect)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");
}

void loop() {

  labelFile = SD.open("TL_G1.TXT");
  dataFile = SD.open("YM_G1.TXT");

  int l_index = 0;
  int labels[DATA_LEN];

  while (labelFile.available())
  {
    char lChar = labelFile.read();     
        if(lChar != '\n')
        {     
 //         Serial.println(lChar-'0');       
    labels[l_index] = lChar-'0'; // single char to int conversion
    l_index++;
        }
  }

//   for (int rr = 0; rr < l_index; ++rr) {
//    Serial.println(labels[rr]); }

//----------------------------------------------------------

    int p_index = 0;
    int pred_labels[l_index];

    while (dataFile.available())
    {

    char datafileContents[24]; // Probably can be smaller
    float data[DATA_LEN];
    float ex_features[FEATURE_LEN];
    float Mtemp = 0;
    float mean = 0;
    float var = 0;
    float std = 0;
    float median = 0;
    float first_q = 0;
    float third_q = 0;
    float iqr = 0;
    float maxv = 0;
    float minv = 0;
    float abslargest = 0;
    int left = 0;
    int right = DATA_LEN - 1;
    byte index = 0;
    int data_index = 0;


      
      while (data_index < DATA_LEN) {

        char dChar = dataFile.read();
        datafileContents[index++] = dChar;
        //   datafileContents[index] = '\0'; // NULL terminate the array DO I NEED THIS LINE?

        if ((dChar == '\n') || (dChar == ','))
        {
          if (strlen(datafileContents) > 0)
          {
            data[data_index] = atof(datafileContents);
            //      Serial.println(data[data_index], 12);
            data_index++;
          }
          datafileContents[0] = '\0';
          index = 0;
        }
      }
   
      quickSort(data, left, right);

      //  for (int tt = 0; tt < DATA_LEN; ++tt)
      //  {Serial.println(data[tt]);
      //  }

      for ( int l = 0; l < DATA_LEN; ++l) {
        float delta = data[l] - mean;
        mean += delta / (l + 1);
        Mtemp += delta * (data[l] - mean);
        var = Mtemp / (l + 1);
      }


      Serial.print("Entry number: ");
      Serial.println(p_index);

      std = sqrt(var);
      Serial.print("The mean value is: ");
      Serial.println(mean);
      Serial.print("The standard deviation is: ");
      Serial.println(std);

      if (DATA_LEN % 2) {
        int m = DATA_LEN / 2;
        median = data[m];

        if (m % 2) {
          first_q = (data[m / 2 ] + data[m / 2 + 1]) / 2;
          third_q = (data[DATA_LEN - (m / 2) - 2] + data[DATA_LEN - (m / 2) - 1]) / 2;
//          Serial.println("waawaaweewaa");
        }
        else {
          first_q = (data[m / 2]);
          third_q = data[DATA_LEN - (m / 2 + 1)];
//          Serial.println("kinginthecastle");
        }
      }
      else {
        int leftm = DATA_LEN / 2 - 1;
        int rightm = DATA_LEN / 2;
        median = (data[leftm] + data[rightm]) / 2;
        if (leftm % 2 == 0 ) {
          first_q = (data[leftm / 2]);
          third_q = data[DATA_LEN - (rightm / 2) - 1];
//          Serial.println("gypsytears");
        }
        else {
          first_q = (data[leftm / 2 ] + data[leftm / 2 + 1]) / 2;
          third_q = (data[DATA_LEN - (rightm / 2)] + data[DATA_LEN - (rightm / 2) - 1]) / 2;
//          Serial.println("uktarthehawk");

        }
      }

      iqr = (third_q - first_q);
      Serial.print("The median value is: ");
      Serial.println(median);
      Serial.print("The first quartile value is: ");
      Serial.println(first_q);
      Serial.print("The third quartile value is: ");
      Serial.println(third_q);
      Serial.print("The inter-quartile range value is: ");
      Serial.println(iqr);

      minv = data[left];
      maxv = data[right];
      if (abs(maxv) >= abs(minv))
      {
        abslargest = maxv;
      }
      else {
        abslargest = abs(minv);
      }

      Serial.print("The min value is: ");
      Serial.println(minv);
      Serial.print("The max value is: ");
      Serial.println(maxv);
      Serial.print("The abslargest value is: ");
      Serial.println(abslargest);

     

      ex_features[0] = mean;
      ex_features[1] = std;
      ex_features[2] = median;
      ex_features[3] = abslargest;
      ex_features[4] = iqr;

      int pred_label = classifier_to_test_float_G1_predict(ex_features, FEATURE_LEN);
      pred_labels[p_index] = pred_label;
      
      Serial.print("Real Label: ");
      Serial.println(labels[p_index]);
      Serial.print("Predicted Label: ");
      Serial.println(pred_label);
      ++p_index;
      Serial.println("---------------------");
  }

 Serial.println("---------------------");
int correct = 0;
for (int acc = 0; acc <p_index; ++acc){
   if (labels[acc] == pred_labels[acc]) {
      ++correct;
    }
}

  Serial.println(correct);
  Serial.println(p_index);

  float accuracy = (float(correct) / float(p_index));
  Serial.print("Accuracy: ");
  Serial.println(accuracy, 3);
  delay(2000);
 Serial.println("---------------------");

 }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
 
