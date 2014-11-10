#!/usr/bin/env pyhton
'''
This file does some ETL operations on the data such as 
    1. Printing Number of Unique values in each column
    2. Removing NULL values and writting the data to a NULL-removed CSV format.
'''
def create_schema(filename):
    for line in file:
        line = line.strip().lower();
        colname = line.split()[0]

def print_unique(filename,feature_stats_filename):
'''This reads in the values of the data in CSV format and prints the unique counts for
each column that is there'''
    with open(filename,'r') as datafile:
        header = datafile.readline();
        cols = header.strip().split(',');
        for line in datafile:
            values = line.strip().split(',');
            data += [values];
        
    #now the data is ready in the list data. fill in missing values and count 
    # the unique values
    unique=fill_missing(data);
    
    #now , after filling the missing data values and calculating the unique counts
    # of each column, print these statistics to a file
    print_feature_stats(feature_stats_filename);


def print_feature_stats(uniqe_data,data,attrkey,feature_stats_filename):
'''This funciton takes in feature unique counts and prints the feauture stats for 
    each feature in the raw_data'''
    numrows = len(data[1:]);
    headers = data[0];
    file = open(feature_stats_filename,'r');
    numcols = headers(features);
    #featire_idx will contain a mapping of dict[attrval]-->attribute index in the higher dim space.
    feature_idx = 0;    
    feature_map = [];

    for j in xrange(numcols):
        print >>file, "FeatureName:%s",headers[j];
        print >>file, "Type:",attrkey[i];
        # for nominal values print name,type,range of attr indices this maps to and distribution
        if attrkey[i]=='nominal':
            num_uniq_vals = len(unique[j]);
            frange=(feature_idx,feature_idx+num_uniq_vals-1); 
            feature_idx += num_uniq_vals;
            fstats = [(key,double(val)/numrows) for key,value in unique[j]];
            attr_rep = zip(fstats,range(frange[0],frange[1]+1));
            attr_map = {};
            print >>file, "FeatureName:",headers[j];
            print >>file, "Type:nominal";
            print >>file, "AttrIdxRange:(%d,%d)"%frange;
            print >>file, "AttrDist:";
            for attr in attr_rep:
                print >>file, "\t(%s,%.3f,%d)"%(attr_rep[0][0],attr_rep[0][1],attr_rep[1]);
                attr_map[attr[0]]=attr[2];
            feature_map += [attr_map];
        # for numeric attrs, print name, type, idx this maps to and the min,max.
        else if attrkey[j]=='numeric':  
            keys = unique[j].keys();
            keys = [double(key) for key in keys];
            max_k = max(keys);
            min_k = min(keys); 
            frange = (feature_idx,feature_idx);
            feature_idx+=1;
            attr_map = {None:frange[0]};
            print >>file, "AttrIdxRange:",frange[0];
            print >>file, "AttrDist:\n\t(%.3f,%.3f)"%(max_k,min_k);
        feature_map += [attr_map];

    file.close();
    return feature_map;


def map_data_to_new_features(data,attrkey,feature_map,new_feature_filename):
'''This takes in the data and the new feature mapping and builds a csv file with 
    the features in the old data mapped to new attributes in higher dim space'''
    headers = data[0];
    numcols = len(headers);
    for row in data[1;]:
        for j in xrange(numcols):
            if attrkey[j]=='nominal':
                num_attrs = len(feature_map[j]);
                vector = [0 for i in xrange(num_attrs)];
                vector[feature_map[j][row[j]]]
                print file,("%d,"*num_attrs)%tuple(vector),

def fil_missing(data,attrkey):
'''Fill in the missing values in the data as follows:
    1.If attribute is numeric , then replace missing values with mean,
    2.If atttribute is nominal , replace missing values with other.
'''
    header = data[0];
    numcols = len(header);
    numrows = len(data);
    unique = [{} for j in xrange(numcols)];
    nullpos = [[] for j in xrange(numcols)];
    for i in xrange(numrows):
        for j in xrange(numcols):
            if data[i][j]=='NULL':
                nullpos[j] += [i];
            else if data[i] in unique[j]:
                unique[j] +=1;
            else: 
                unique[j][data[i]] = 1;
                
    for j in xrange(numcols):
        if attrkey[j]=='nominal':
            #mod_val = max(unique[j].iteritems(),key=operator.itemgetter(1))[0];
            for pos in nullpos[j]:
                data[pos][j]='other';
            #add the counts for other as well as now it is also a valid value
            unique[i]['other'] = len(nullpos[j]);
        else if attrkey[j]=='numeric':
                total_sum = 0;
                total_freq = 0;
                for (x,f) in unique[j].items():
                    total_sum += double(x)*double(f);
                    total_freq += double(f);
                mean_val = total_sum/total_freq;                    
            for pos in nullpos[j]:
                data[pos][j] = str(mean_val);
    
    return unique; 
    
