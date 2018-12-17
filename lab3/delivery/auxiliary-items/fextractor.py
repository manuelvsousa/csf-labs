import os
import argparse
import numpy

#CSF1819: 
    #Here you should add more features to the feature vector (features=[]) representing a cell trace

    #Function extract receives as input two sequences:
    #    times: timestamp of each cell
    #    sizes: direction of each cell (-1 / +1)

    #As of now, the only feature being used to distinguish between page loads is the total
    # amount of cells in each cell sequence and is given by len(times).

    # Shall some feature be missing due to impossibility of its calculation, 
    #please replace its value with "X". It will be replaced later.

def bucketizeCounter(feature, buckets):
    ret = [0 for i in buckets]
    for f in feature:
        for j in range(len(buckets)):
            if (buckets[j][0] <= f and f <= buckets[j][1]):
                ret[j] += 1
    return ret

def binarize(feature, thresh=1):
    ret = [1 if i >= thresh else 0 for i in feature]
    return ret

def normalize(bucket):
    if (len(bucket)==0):
        return []
    maxBucketSz = max(bucket)
    if (maxBucketSz==0):
        return bucket
    return [x//maxBucketSz for x in bucket]


def extract(times, sizes):
    features = []

    posIndexOut = [i for i in range(len(sizes)) if sizes[i]>0]
    posIndexIn = [i for i in range(len(sizes)) if sizes[i]<0]

    assert(len(times) == len(sizes))
    #number of packets
    features.append(len(times))
    #transmission time
    features.append(times[-1] - times[0])
    #incoming/outgoing packets distribution
    features += bucketizeCounter(sizes, [(-1,-1),(1,1)])
    
    features += posIndexIn[:100] + ["X" for i in range(len(posIndexIn[:100]), 100)]
    features += posIndexOut[:100] + ["X" for i in range(len(posIndexOut[:100]), 100)]
    

    for i in range(0, min(len(sizes),50)):
        features.append(sizes[i] + 1)
    for i in range(i,50):
        features.append("X")
    
    #Deltas between outgoings
    outDeltas = []
    for i in range(1, min(len(posIndexOut), 30)):
        outDeltas.append(posIndexOut[i] - posIndexOut[i-1])
    
    #Delta times between outgoings
    outDeltasTime = []
    for i in range(1, min(len(posIndexOut), 30)):
        outDeltasTime.append(times[posIndexOut[i]] - times[posIndexOut[i-1]])
    
    #Deltas between ingoings
    inDeltas = []
    for i in range(1, min(len(posIndexIn), 30)):
        inDeltas.append(posIndexIn[i] - posIndexIn[i-1])
    
    #Delta times between ingoings
    inDeltasTime = []
    for i in range(1, min(len(posIndexIn), 30)):
        inDeltasTime.append(times[posIndexIn[i]] - times[posIndexIn[i-1]])

    features += normalize(inDeltasTime) + ["X" for i in range(len(inDeltasTime), 30)]
    features += normalize(outDeltasTime) + ["X" for i in range(len(outDeltasTime), 30)]
    features += inDeltas + ["X" for i in range(len(inDeltas), 30)]
    features += outDeltas + ["X" for i in range(len(outDeltas), 30)]

    buckets = [ (0,1),
                (2,3),
                (4,6),
                (7,10),
                (11,15),
                (16,21),
                (22,28),
                (29,36),
                (37,45),
                (45,54),
                (55,65),
                (65,10000)
    ]
    if (len(outDeltas) > 0):
        features.append(max(outDeltas))
        features.append(numpy.mean(outDeltas))
        features.append(len(outDeltas))
        features.append(numpy.mean(outDeltasTime))
        features.append(numpy.std(outDeltasTime))
        features.append(numpy.min(outDeltasTime))
        features.append(numpy.max(outDeltasTime))

        features += bucketizeCounter(outDeltas, buckets)
    else:
        for i in range(7 + len(buckets)):
            features.append('X')
        
    if (len(inDeltas) > 0):
        features.append(max(inDeltas))
        features.append(numpy.mean(inDeltas))
        features.append(len(inDeltas))
        features.append(numpy.mean(inDeltasTime))
        features.append(numpy.std(inDeltasTime))
        features.append(numpy.min(inDeltasTime))
        features.append(numpy.max(inDeltasTime))

        features += bucketizeCounter(inDeltas, buckets)
    else:
        for i in range(7+len(buckets)):
            features.append('X')
    
    #Packet distributions (random metric from wang)
    for i in range(0, min(len(sizes), 300), 30):
        count = 0
        for k in range(i, min(len(sizes), i+30)):
            if sizes[k] > 0:
                count += 1
        features.append(count)
    for i in range(i, 300, 30):
        features.append('X')

    if (len(posIndexOut)!=0):
        posIndexOut = [posIndexOut[0]] + [posIndexOut[i] for i in range(1,len(posIndexOut)) if (posIndexOut[i]-1 != posIndexOut[i-1])]
    if (len(posIndexIn)!=0):
        posIndexIn = [posIndexIn[0]] + [posIndexIn[i] for i in range(1,len(posIndexIn)) if (posIndexIn[i]-1 != posIndexIn[i-1])]

    posIndexIn = posIndexIn[:30] 
    posIndexOut = posIndexOut[:30]    
    features += posIndexIn + ["X" for i in range(len(posIndexIn), 30)]
    features += posIndexOut + ["X" for i in range(len(posIndexOut), 30)]
    

     

    return features


def impute_missing(x):
        """Accepts a list of features containing 'X' in
        place of missing values. Consistently with the code
        by Cao et al, replaces 'X' with -1.
        """
        for i in range(len(x)):
            if x[i] == 'X':
                x[i] = -1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract feature vectors')
    parser.add_argument('--traces', type=str, help='Original traces directory.',
                        required=True)
    parser.add_argument('--out', type=str, help='Output directory for features.',
                        required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.out):
        os.makedirs(args.out)

    #this takes quite a while
    print "Gathering features for monitored sites..."
    for site in range(0, 100):
        print site
        for instance in range(0, 90):
            fname = str(site) + "-" + str(instance)
            #Set up times, sizes
            f = open(args.traces + "/" + fname, "r")
            times = []
            sizes = []
            for x in f:
                x = x.split("\t")
                times.append(float(x[0]))
                sizes.append(int(x[1]))
            f.close()
    
            #Extract features. All features are non-negative numbers or X. 
            features = extract(times, sizes)

            #Replace X by -1 (Cai et al.)
            impute_missing(features)

            fout = open(args.out + "/" + fname + ".features", "w")
            for x in features[:-1]:
                fout.write(repr(x) + ",")
            fout.write(repr(features[-1]))
            fout.close()

    print "Finished gathering features for monitored sites."

    print "Gathering features for non-monitored sites..."
    #open world
    for site in range(0, 9000):
        print site
        fname = str(site)
        #Set up times, sizes
        f = open(args.traces + "/" + fname, "r")
        times = []
        sizes = []
        for x in f:
            x = x.split("\t")
            times.append(float(x[0]))
            sizes.append(int(x[1]))
        f.close()
    
        #Extract features. All features are non-negative numbers or X. 
        features = extract(times, sizes)

        #Replace X by -1 (Cai et al.)
        impute_missing(features)

        fout = open(args.out + "/" + fname + ".features", "w")
        for x in features[:-1]:
            fout.write(repr(x) + ",")
        fout.write(repr(features[-1]))
        fout.close()

    print "Finished gathering features for non-monitored sites."
    f.close()
