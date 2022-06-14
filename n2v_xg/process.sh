organism="$1"

# for dim in 32
# do
#     for epochs in 1
#     do
#         for length in 120
#         do
#             for walk in 20
#             do
#                 for cont in 10
#                 do
#                     for retpar in 1
#                     do
#                         ./node2vec -i:../data/${organism}_ppi_graph.txt -o:emb/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb -d:${dim} -e:${epochs} -l:${length} -r:${walk} -k:${cont} -p:${retpar}
#                     done
#                 done
#             done
#         done
#     done
# done


echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef,Roc_Auc,Precision,Recall" > log/${organism}_results.csv

for dim in 32
do
    for epochs in 1
    do
        for length in 120
        do
            for walk in 20
            do
                for cont in 10
                do
                    for retpar in 1
                    do
                        FILE="${PWD}/emb/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb"
                        if [ -f $FILE ]; then
                            echo "$FILE exists"
                            python3 remix.py $FILE $organism &
                            wait
                            for option in 1 2
                            do
                                python3 embedding.py ${FILE} ${option} ${organism}
                                log_file="log/${organism}_last${option}.csv"
                                echo -n "${dim},${epochs},${length},${walk},${cont},${retpar}," >> $log_file
                                
                                emb_filename="csv_imp/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb.csv"
                                es_filename="csv_imp/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb_out.csv"
                                python3 boost.py $emb_filename $es_filename $option >> $log_file                                
                           done
                        fi
                    done
                done
            done
        done
    done
done